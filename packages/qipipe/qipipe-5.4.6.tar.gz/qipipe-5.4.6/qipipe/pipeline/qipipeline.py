import os
import re
import tempfile
import logging
from collections import defaultdict
from nipype.pipeline import engine as pe
from nipype.interfaces.utility import (IdentityInterface, Function, Merge)
from nipype.interfaces.dcmstack import MergeNifti
import qixnat
from qixnat.helpers import path_hierarchy
from qiutil.logging import logger
import qipipe
from . import staging
from .workflow_base import WorkflowBase
from .staging import StagingWorkflow
from .mask import MaskWorkflow
from .roi import ROIWorkflow
import registration
from ..interfaces import (XNATDownload, XNATUpload)
from ..staging.iterator import iter_stage
from ..staging.map_ctp import map_ctp
from ..staging.roi import iter_roi
# OHSU - multi-volume scans.
from ..staging.ohsu import MULTI_VOLUME_SCAN_NUMBERS

SCAN_TS_RSC = 'scan_ts'
"""The XNAT scan time series resource name."""

MASK_RSC = 'mask'
"""The XNAT mask resouce name."""

VOLUME_FILE_PAT = re.compile("volume(\d{3}).nii.gz$")
"""The volume image file name pattern."""

ACTIONS = ['stage', 'roi', 'register', 'model']
"""The list of all available actions."""


def run(*inputs, **opts):
    """
    Creates a :class:`qipipe.pipeline.qipipeline.QIPipelineWorkflow`
    and runs it on the given inputs, as follows:

    - If the *actions* option includes ``stage`` or ``roi``, then
      the input is the :meth:`QIPipelineWorkflow.run_with_dicom_input`
      DICOM subject directories input.

    - Otherwise, the input is the
      :meth:`QIPipelineWorkflow.run_with_scan_download` XNAT session
      labels input.

    :param inputs: the input directories or XNAT session labels to
        process
    :param opts: the :meth:`qipipe.staging.iterator.iter_stage`
        and :class:`QIPipelineWorkflow` initializer options,
        as well as the following keyword options:
    :keyword project: the XNAT project name
    :keyword collection: the image collection name
    :keyword actions: the workflow actions to perform
    :keyword resume: flag indicating whether to resume processing on
        existing sessions (default False)
    """
    # The actions to perform.
    actions = opts.pop('actions', _default_actions(**opts))
    if 'stage' in actions:
        # Run with staging DICOM subject directory input.
        _run_with_dicom_input(actions, *inputs, **opts)
    elif 'roi' in actions:
        # The non-staging ROI action must be performed alone.
        if len(actions) > 1:
            raise ArgumentError("The ROI pipeline can only be run with"
                                " staging or stand-alone")
        _run_with_dicom_input(actions, *inputs, **opts)
    else:
        # Run downstream actions with XNAT session input.
        _run_with_xnat_input(actions, *inputs, **opts)


def _default_actions(**opts):
    """
    Returns the default actions from the given options, as follows:

    * If the *registration* resource option is set, then the actions
      consist of ``register`` and ``model``.

    * Otherwise, all of the actions in :const:`ACTIONS` are performed.

    :param opts: the :meth:`run` options
    :return: the default actions
    """
    if 'registration' in opts:
        return ['register', 'model']
    else:
        return ACTIONS


def _run_with_dicom_input(actions, *inputs, **opts):
    """
    :param actions: the actions to perform
    :param inputs: the DICOM directories to process
    :param opts: the :meth:`run` options
    """
    # The required XNAT project name.
    project = opts.pop('project', None)
    if not project:
        raise ArgumentError('The staging pipeline project option is missing.')
    # The required image collection name.
    collection_opt = opts.pop('collection', None)
    if not collection_opt:
        raise ArgumentError('The staging pipeline collection option is missing.')
    # The collection name is capitalized.
    collection = collection_opt.capitalize()
    # The target directory.
    dest = opts.get('dest', None)
    # The resume option corresponds to the staging helper iter_stage
    # function skip_existing option.
    if opts.pop('resume', None):
        opts['skip_existing'] = False

    # The set of input subjects is used to build the CTP mapping file
    # after the workflow is completed, if staging is enabled.
    subjects = set()
    # Run the workflow on each session and scan.
    for scan_input in iter_stage(project, collection, *inputs, **opts):
        # OHSU - Only multi-volume scans can have post-staging downstream
        # actions.
        if len(scan_input.iterators.dicom) == MULTI_VOLUME_SCAN_NUMBERS:
            if 'stage' in actions:
                wf_actions = ['stage']
            else:
                continue
        else:
            wf_actions = actions
        # Capture the subject.
        subjects.add(scan_input.subject)
        # Create a new workflow.
        wf_gen = QIPipelineWorkflow(project, wf_actions, **opts)
        # Run the workflow on the scan.
        wf_gen.run_with_dicom_input(wf_actions, scan_input, dest)

    # If staging is enabled, then make the TCIA subject map.
    if 'stage' in actions:
        map_ctp(collection, *subjects, dest=dest)


def _run_with_xnat_input(actions, *inputs, **opts):
    """
    Run the pipeline with a XNAT download. Each input is a XNAT scan
    path, e.g. ``/QIN/Breast012/Session03/scan/1``.

    :param actions: the actions to perform
    :param inputs: the XNAT scan resource paths
    :param opts: the :class:`QIPipelineWorkflow` initializer options
    """
    with qixnat.connect() as xnat:
        for path in inputs:
            hierarchy = dict(path_hierarchy(path))
            prj = hierarchy.pop('project', None)
            if not prj:
                raise ArgumentError("The XNAT path is missing a project: %s" % path)
            sbj = hierarchy.pop('subject', None)
            if not sbj:
                raise ArgumentError("The XNAT path is missing a subject: %s" % path)
            sess = hierarchy.pop('experiment', None)
            if not sess:
                raise ArgumentError("The XNAT path is missing a session: %s" % path)
            scan_s = hierarchy.pop('scan', None)
            if not scan_s:
                raise ArgumentError("The XNAT path is missing a scan: %s" % path)
            scan = int(scan_s)
            # The XNAT scan object must exist.
            scan_obj = xnat.find_one(prj, sbj, sess, scan=scan)
            if not scan_obj:
                raise ArgumentError("The XNAT scan object does not exist: %s" % path)
            
            # The workflow options are augmented from the base options.
            wf_opts = dict(opts)
            # Check for an existing mask.
            if _scan_resource_exists(prj, sbj, sess, scan, MASK_RSC):
                wf_opts['mask'] = MASK_RSC

            # Every post-stage action requires a 4D scan time series.
            ts_actions = (action for action in actions if action != 'stage')
            if any(ts_actions):
                if _scan_resource_exists(prj, sbj, sess, scan, SCAN_TS_RSC):
                    wf_opts['scan_time_series'] = SCAN_TS_RSC

            # If modeling will be performed on a specified registration
            # resource, then check for an existing 4D registration time series.
            if 'model' in actions and 'registration' in opts:
                reg_ts_rsc = opts['registration'] + '_ts'
                if _scan_resource_exists(prj, sbj, sess, scan, reg_ts_rsc):
                    wf_opts['realigned_time_series'] = reg_ts_rsc

            # Execute the workflow.
            wf_gen = QIPipelineWorkflow(prj, actions, **wf_opts)
            wf_gen.run_with_scan_download(xnat, prj, sbj, sess, scan)


def _scan_resource_exists(project, subject, session, scan, resource):
    """
    :return: whether the given XNAT scan resource exists
    """
    with qixnat.connect() as xnat:
        rsc_obj = xnat.find_one(project, subject, session, scan=scan,
                            resource=resource)
    exists = rsc_obj and rsc_obj.files().get()
    status = 'found' if exists else 'not found'
    logger(__name__).debug("The %s %s %s scan %d resource %s was %s." %
                           (project, subject, session, scan, resource, status))

    return exists


class ArgumentError(Exception):
    pass


class NotFoundError(Exception):
    pass


class QIPipelineWorkflow(WorkflowBase):
    """
    QIPipeline builds and executes the imaging workflows. The pipeline
    builds a composite workflow which stitches together the following
    constituent workflows:

    - staging: Prepare the new DICOM visits, as described in
      :class:`qipipe.pipeline.staging.StagingWorkflow`

    - mask: Create the mask from the staged images,
      as described in :class:`qipipe.pipeline.mask.MaskWorkflow`

    - registration: Mask, register and realign the staged images,
      as described in
      :class:`qipipe.pipeline.registration.RegistrationWorkflow`

    - modeling: Perform PK modeling as described in
      :class:`qipipe.pipeline.modeling.ModelingWorkflow`

    The constituent workflows are determined by the initialization
    options ``stage``, ``register`` and ``model``. The default is
    to perform each of these subworkflows.

    The workflow steps are determined by the input options as follows:

    - If staging is performed, then the DICOM files are staged for the
      subject directory inputs. Otherwise, staging is not performed.
      In that case, if registration is enabled as described below, then
      the previously staged volume scan stack images are downloaded.

    - If registration is performed and the ``registration`` resource option
      is set, then the previously realigned images with the given resource
      name are downloaded. The remaining volumes are registered.

    - If registration or modeling is performed and the XNAT ``mask``
      resource is found, then that resource file is downloaded. Otherwise,
      the mask is created from the staged images.

    The QIN workflow input node is *input_spec* with the following
    fields:

    - *subject*: the subject name

    - *session*: the session name

    - *scan*: the scan number

    In addition, if the staging or registration workflow is enabled
    then the *iter_volume* node iterables input includes the
    following fields:

    - *volume*: the scan number

    - *dest*: the target staging directory, if the staging
      workflow is enabled

    The constituent workflows are combined as follows:

    - The staging workflow input is the QIN workflow input.

    - The mask workflow input is the newly created or previously staged
      scan NiFTI image files.

    - The modeling workflow input is the combination of the previously
      uploaded and newly realigned image files.

    The pipeline workflow is available as the
    :attr:`qipipe.pipeline.qipipeline.QIPipelineWorkflow.workflow`
    instance variable.
    """

    def __init__(self, project, actions, **opts):
        """
        :param project: the XNAT project name
        :param actions: the actions to perform
        :param opts: the :class:`qipipe.staging.WorkflowBase`
            initialization options as well as the following options:
        :keyword mask: the XNAT mask resource name
        :keyword registration_resource: the XNAT registration resource name
        :keyword registration_technique: the
            class:`qipipe.pipeline.registration.RegistrationWorkflow`
            technique
        :keyword modeling_resource: the modeling resource name
        :keyword modeling_technique: the
            class:`qipipe.pipeline.modeling.ModelingWorkflow` technique
        """
        super(QIPipelineWorkflow, self).__init__(project, logger(__name__), **opts)

        self.registration_resource = None
        """The registration XNAT resource name."""

        self.modeling_resource = None
        """The modeling XNAT resource name."""

        self.workflow = self._create_workflow(actions, **opts)
        """
        The pipeline execution workflow. The execution workflow is executed
        by calling the :meth:`run_with_dicom_input` or
        :meth:`run_with_scan_download` method.
        """

    def run_with_dicom_input(self, actions, scan_input, dest=None):
        """
        :param actions: the workflow actions to perform
        :param scan_input: the :class:`qipipe.staging.iterator.ScanInput`
            object
        :param dest: the TCIA staging destination directory (default is
            the current working directory)
        """
        # Set the workflow input.
        input_spec = self.workflow.get_node('input_spec')
        input_spec.inputs.collection = scan_input.collection
        input_spec.inputs.subject = scan_input.subject
        input_spec.inputs.session = scan_input.session
        input_spec.inputs.scan = scan_input.scan
        
        # If staging is enabled, then set the staging iterables.
        if 'stage' in actions:
            staging.set_workflow_iterables(self.workflow, scan_input, dest)
        # If roi is enabled and has input, then set the roi function inputs.
        if 'roi' in actions and scan_input.iterators.roi:
            self._set_roi_inputs(*scan_input.iterators.roi)
        # Execute the workflow.
        self._logger.debug("Running the pipeline on %s %s scan %d." %
                           (scan_input.subject, scan_input.session,
                            scan_input.scan))
        self._run_workflow(self.workflow)
        self._logger.debug("Completed pipeline execution on %s %s scan %d." %
                           (scan_input.subject, scan_input.session,
                            scan_input.scan))

    def run_with_scan_download(self, xnat, project, subject, session, scan):
        """
        Runs the execution workflow on downloaded scan image files.
        """
        self._logger.debug("Processing the %s %s %s scan %d scan..." %
                           (project, subject, session, scan))

        # Get the volume numbers.
        scan_obj = xnat.find_one(project, subject, session, scan=scan)
        if not scan_obj:
            raise NotFoundError("The QIN pipeline did not find a %s %s %s"
                                " scan %d." %
                                (project, subject, session, scan))
        # The NIFTI resource contains the volume files.
        rsc_obj = scan_obj.resource('NIFTI')
        if not rsc_obj.exists():
            raise NotFoundError("The QIN pipeline did not find a %s %s %s"
                                " scan %d NIFTI resource." %
                                (project, subject, session, scan))
        # The volume files.
        files = rsc_obj.files().get()

        # Partition the scan image files into those which are already
        # registered and those which need to be registered.
        reg_files, unreg_files = self._partition_registered(xnat, project,
                                                            subject, session,
                                                            scan, files)

        # Set the workflow input.
        input_spec = self.workflow.get_node('input_spec')
        input_spec.inputs.subject = subject
        input_spec.inputs.session = session
        input_spec.inputs.scan = scan
        input_spec.inputs.in_files = unreg_files

        # Execute the workflow.
        self._run_workflow(self.workflow)
        self._logger.debug("Processed %d %s %s %s scan %d volumes." %
                           (len(volumes), project, subject, session, scan))

    def _set_roi_inputs(self, *inputs):
        """
        :param collection: the image collection name
        :param subject: the subject name
        :param session: the session name
        :param scan: the scan number
        :param inputs: the :meth:`roi` inputs
        """
        # Set the roi function inputs.
        roi_node = self.workflow.get_node('roi')
        roi_node.inputs.in_rois = inputs
        roi_node.inputs.opts = dict(base_dir=self.workflow.base_dir)

    def _partition_registered(self, xnat, project, subject, session, scan, files):
        """
        Partitions the given volume file names into those which have a
        corresponding registration resource file and those which
        don't.

        :return: the (registered, unregistered) file names
        """
        # The XNAT registration object.
        if self.registration_resource:
            reg_obj = xnat.find_one(project, subject, session, scan=scan,
                                    resource=self.registration_resource)
        else:
            reg_obj = None
        # If the registration has not yet been performed, then
        # download all of the volumes.
        if not reg_obj:
            return [], files

        # The realigned files.
        reg_files = set(reg_obj.files().get())
        # The unregistered volume numbers.
        unreg_files = set(files) - reg_files
        self._logger.debug("The %s %s %s resource has %d registered volumes"
                           " and %d unregistered volumes." %
                           (project, subject, session, len(reg_files),
                            len(unreg_files)))

        return reg_files, unreg_files

    def _create_workflow(self, actions, **opts):
        """
        Builds the reusable pipeline workflow described in
        :class:`qipipe.pipeline.qipipeline.QIPipeline`.

        :param actions: the actions to perform
        :param opts: the constituent workflow initializer options
        :return: the Nipype workflow
        """

        # This is a long method body with the following stages:
        #
        # 1. Gather the options.
        # 2. Create the constituent workflows.
        # 3. Tie together the constituent workflows.
        #
        # The constituent workflows are created in back-to-front order,
        # i.e. modeling, registration, mask, roi, staging.
        # This order makes it easier to determine whether to create
        # an upstream workflow depending on the presence of downstream
        # workflows, e.g. the mask is not created if registration
        # is not performed.
        #
        # By contrast, the workflows are tied together in front-to-back
        # order.

        self._logger.debug("Building the QIN pipeline execution workflow"
                            " for the actions %s..." % actions)
        # The execution workflow.
        exec_wf = pe.Workflow(name='qipipeline', base_dir=self.base_dir)

        # The workflow options.
        mask_rsc = opts.get('mask')
        scan_ts_rsc = opts.get('scan_time_series')
        reg_ts_rsc = opts.get('realigned_time_series')
        reg_rsc = opts.get('registration_resource')
        reg_technique = opts.get('registration_technique')
        mdl_rsc = opts.get('modeling_resource')
        mdl_technique = opts.get('modeling_technique')

        # Set the registration resource instance variable.
        if reg_rsc:
            self.registration_resource = reg_rsc

        # The modeling workflow. Since the proprietary fastfit module might
        # not be available, only import the ModelingWorkflow on demand if
        # modeling is required.
        if 'model' in actions:
            from .modeling import ModelingWorkflow
            mdl_opts = dict(project=self.project, base_dir=self.base_dir)
            if mdl_rsc:
                mdl_opts['resource'] = mdl_rsc
            if mdl_technique:
                mdl_opts['technique'] = mdl_technique
            mdl_wf_gen = ModelingWorkflow(**mdl_opts)
            mdl_wf = mdl_wf_gen.workflow
            self.modeling_resource = mdl_wf_gen.resource
        else:
            mdl_wf = None

        # The registration workflow node.
        if 'register' in actions:
            reg_inputs = ['project', 'subject', 'session', 'scan',
                          'bolus_arrival_index', 'in_files', 'mask',
                          'opts']

            # The registration function keyword options.
            reg_opts = dict(base_dir=self.base_dir)
            if reg_technique:
                reg_opts['technique'] = reg_technique
            # If the resource was not specified, then make a new
            # resource name.
            if not reg_rsc:
                new_reg_rsc = registration.generate_resource_name()
                self.registration_resource = new_reg_rsc
            # Add the resource name to the registration options.
            reg_opts['resource'] = self.registration_resource

            # The registration function.
            reg_xfc = Function(input_names=reg_inputs,
                               output_names=['out_files'],
                               function=register)
            reg_node = pe.Node(reg_xfc, name='register')
            reg_node.inputs.project = self.project
            reg_node.inputs.opts = reg_opts
            self._logger.info("Enabled registration.")
        else:
            self._logger.info("Skipping registration.")
            reg_node = None

        # The ROI workflow node.
        if 'roi' in actions:
            roi_inputs = ['project', 'subject', 'session', 'scan',
                          'time_series', 'in_rois', 'opts']
            roi_xfc = Function(input_names=roi_inputs, output_names=[],
                               function=roi)
            roi_node = pe.Node(roi_xfc, name='roi')
            roi_node.inputs.project = self.project
            roi_node.opts = dict(base_dir=self.base_dir)
            self._logger.info("Enabled ROI conversion.")
        else:
            roi_node = None
            self._logger.info("Skipping ROI conversion.")

        # Registration and modeling require a mask.
        if (reg_node or mdl_wf) and not mask_rsc:
            mask_wf_gen = MaskWorkflow(project=self.project)
            mask_wf = mask_wf_gen.workflow
            self._logger.info("Enabled scan mask creation.")
        else:
            mask_wf = None
            self._logger.info("Skipping scan mask creation.")

        # The staging workflow.
        if 'stage' in actions:
            stg_wf_gen = StagingWorkflow(project=self.project)
            stg_wf = stg_wf_gen.workflow
            self._logger.info("Enabled staging.")
        else:
            stg_wf = None
            self._logger.info("Skipping staging.")

        # Validate that there is at least one constituent workflow.
        if not any([stg_wf, roi_node, reg_node, mdl_wf]):
            raise ArgumentError("No workflow was enabled.")

        # The workflow input fields.
        input_fields = ['subject', 'session', 'scan']
        iter_volume_fields = ['volume']
        # The staging workflow has additional input fields.
        # Partial registration requires the unregistered volumes input.
        if stg_wf:
            input_fields.append('collection')
            iter_volume_fields.append('dest')
        elif reg_node and reg_rsc:
            input_fields.append('in_files')

        # The workflow input node.
        input_spec_xfc = IdentityInterface(fields=input_fields)
        input_spec = pe.Node(input_spec_xfc, name='input_spec')
        # Staging, registration, and mask require a volume iterator node.
        # Modeling requires a volume iterator node if and only if the
        # following conditions hold:
        # * modeling is performed on the scan time series, and
        # * the scan time series is not specified
        model_reg = reg_node or reg_ts_rsc
        model_scan = not model_reg
        model_vol = model_scan and not scan_ts_rsc
        if stg_wf or reg_node or mask_wf or (mdl_wf and model_vol):
            iter_volume_xfc = IdentityInterface(fields=iter_volume_fields)
            iter_volume = pe.Node(iter_volume_xfc, name='iter_volume')
        # Staging requires a DICOM iterator node.
        if stg_wf:
            iter_dicom_xfc = IdentityInterface(fields=['volume', 'dicom_file'])
            iter_dicom = pe.Node(iter_dicom_xfc, name='iter_dicom')
            exec_wf.connect(iter_volume, 'volume', iter_dicom, 'volume')

        # Stitch together the workflows:

        # If staging is enabled, then stage the DICOM input.
        if stg_wf:
            for field in input_spec.inputs.copyable_trait_names():
                exec_wf.connect(input_spec, field,
                                stg_wf, 'input_spec.' + field)
            for field in iter_volume.inputs.copyable_trait_names():
                exec_wf.connect(iter_volume, field,
                                stg_wf, 'iter_volume.' + field)
            exec_wf.connect(iter_dicom, 'dicom_file',
                            stg_wf, 'iter_dicom.dicom_file')

        # Some workflows require the scan volumes, as follows:
        # * If staging is enabled, then collect the staged NiFTI
        #   scan images.
        # * Otherwise, if registration is enabled and there is not
        #   yet a scan time series, then download the staged XNAT
        #   scan images.
        # In either of the above cases, the staged images are collected
        # in a node named 'staged' with output 'images', which is used
        # later in the pipeline.
        # Otherwise, there is no staged node.
        if reg_node or roi_node or mask_wf or (mdl_wf and not model_reg):
            if stg_wf:
                staged = pe.JoinNode(IdentityInterface(fields=['out_files']),
                                    joinsource='iter_volume', name='staged')
                exec_wf.connect(stg_wf, 'output_spec.image',
                                staged, 'out_files')
            elif reg_node or not scan_ts_rsc:
                dl_scan_xfc = XNATDownload(project=self.project,
                                           resource='NIFTI')
                staged = pe.Node(dl_scan_xfc, name='staged')
                exec_wf.connect(input_spec, 'subject', staged, 'subject')
                exec_wf.connect(input_spec, 'session', staged, 'session')
                exec_wf.connect(input_spec, 'scan', staged, 'scan')

        # All downstream actions require a scan time series.
        if reg_node or mask_wf or roi_node or mdl_wf:
            # If there is a scan time series, then download it.
            # Otherwise, if staging is enabled, then stack the resulting
            # staged 3D images into the scan time series.
            # Any other case is an error.
            if scan_ts_rsc:
                dl_scan_ts_xfc = XNATDownload(project=self.project,
                                              resource=SCAN_TS_RSC)
                scan_ts = pe.Node(dl_scan_ts_xfc,
                                  name='download_scan_time_series')
                exec_wf.connect(input_spec, 'subject', scan_ts, 'subject')
                exec_wf.connect(input_spec, 'session', scan_ts, 'session')
                exec_wf.connect(input_spec, 'scan', scan_ts, 'scan')
            elif staged:
                # Merge the staged files.
                scan_ts_xfc = MergeNifti(out_format=SCAN_TS_RSC)
                scan_ts = pe.Node(scan_ts_xfc, name='merge_volumes')
                exec_wf.connect(staged, 'out_files', scan_ts, 'in_files')
                self._logger.debug('Connected staging to scan time series merge.')
                # Upload the time series.
                ul_scan_ts_xfc = XNATUpload(project=self.project,
                                            resource=SCAN_TS_RSC,
                                            modality='MR')
                ul_scan_ts = pe.Node(ul_scan_ts_xfc,
                                     name='upload_scan_time_series')
                exec_wf.connect(input_spec, 'subject', ul_scan_ts, 'subject')
                exec_wf.connect(input_spec, 'session', ul_scan_ts, 'session')
                exec_wf.connect(input_spec, 'scan', ul_scan_ts, 'scan')
                exec_wf.connect(scan_ts, 'out_file', ul_scan_ts, 'in_files')
            else:
                raise NotFoundError('The workflow requires a scan time series')

        # Registration and modeling require a mask and bolus arrival.
        if reg_node or mdl_wf:
            # If a mask resource name was specified, then download the mask.
            # Otherwise, make the mask.
            if mask_rsc:
                dl_mask_xfc = XNATDownload(project=self.project,
                                           resource=mask_rsc)
                download_mask = pe.Node(dl_mask_xfc, name='download_mask')
                exec_wf.connect(input_spec, 'subject', download_mask, 'subject')
                exec_wf.connect(input_spec, 'session', download_mask, 'session')
                exec_wf.connect(input_spec, 'scan', download_mask, 'scan')
            else:
                assert mask_wf, "The mask workflow is missing"
                exec_wf.connect(input_spec, 'subject',
                                mask_wf, 'input_spec.subject')
                exec_wf.connect(input_spec, 'session',
                                mask_wf, 'input_spec.session')
                exec_wf.connect(input_spec, 'scan',
                                mask_wf, 'input_spec.scan')
                exec_wf.connect(scan_ts, 'out_file',
                                mask_wf, 'input_spec.time_series')
                self._logger.debug('Connected scan time series to mask.')

            # Compute the bolus arrival from the scan time series.
            bolus_arv_xfc = Function(input_names=['time_series'],
                                     output_names=['bolus_arrival_index'],
                                     function=bolus_arrival_index_or_zero)
            bolus_arv = pe.Node(bolus_arv_xfc, name='bolus_arrival_index')
            exec_wf.connect(scan_ts, 'out_file', bolus_arv, 'time_series')
            self._logger.debug('Connected scan time series to bolus arrival.')

        # If ROI is enabled, then convert the ROIs.
        if roi_node:
            exec_wf.connect(input_spec, 'subject', roi_node, 'subject')
            exec_wf.connect(input_spec, 'session', roi_node, 'session')
            exec_wf.connect(input_spec, 'scan', roi_node, 'scan')
            exec_wf.connect(scan_ts, 'out_file', roi_node, 'time_series')
            self._logger.debug('Connected the scan time series to ROI.')

        # If registration is enabled, then register the staged images.
        if reg_node:
            exec_wf.connect(input_spec, 'subject', reg_node, 'subject')
            exec_wf.connect(input_spec, 'session', reg_node, 'session')
            exec_wf.connect(input_spec, 'scan', reg_node, 'scan')
            # The staged input.
            if stg_wf or not reg_rsc:
                # Register all staged files.
                exec_wf.connect(staged, 'out_files', reg_node, 'in_files')
                self._logger.debug('Connected staging to registration.')
            else:
                # Register only the unregistered files.
                exec_wf.connect(input_spec, 'in_files',
                                reg_node, 'in_files')
            # The mask input.
            if mask_wf:
                exec_wf.connect(mask_wf, 'output_spec.mask', reg_node, 'mask')
                self._logger.debug('Connected mask to registration.')
            else:
                exec_wf.connect(download_mask, 'out_file', reg_node, 'mask')
            # The bolus arrival.
            exec_wf.connect(bolus_arv, 'bolus_arrival_index',
                            reg_node, 'bolus_arrival_index')
            self._logger.debug('Connected bolus arrival to registration.')

        # If the modeling workflow is enabled, then model the scan or realigned
        # images.
        if mdl_wf:
            exec_wf.connect(input_spec, 'subject',
                            mdl_wf, 'input_spec.subject')
            exec_wf.connect(input_spec, 'session',
                            mdl_wf, 'input_spec.session')
            exec_wf.connect(input_spec, 'scan',
                            mdl_wf, 'input_spec.scan')
            # The mask input.
            if mask_wf:
                exec_wf.connect(mask_wf, 'output_spec.mask',
                                mdl_wf, 'input_spec.mask')
                self._logger.debug('Connected mask to modeling.')
            else:
                exec_wf.connect(download_mask, 'out_file',
                                mdl_wf, 'input_spec.mask')
            # The bolus arrival.
            exec_wf.connect(bolus_arv, 'bolus_arrival_index',
                            mdl_wf, 'input_spec.bolus_arrival_index')
            self._logger.debug('Connected bolus arrival to modeling.')

            # If registration is enabled, then the registration 4D
            # time series is created by that workflow, otherwise
            # download the previously created time series.
            if reg_ts_rsc:
                # Download the XNAT time series file.
                ts_dl_xfc = XNATDownload(project=self.project,
                                         resource=reg_ts_rsc)
                reg_ts = pe.Node(ts_dl_xfc, name='download_reg_time_series')
                exec_wf.connect(input_spec, 'subject', reg_ts, 'subject')
                exec_wf.connect(input_spec, 'session', reg_ts, 'session')
                exec_wf.connect(input_spec, 'scan', reg_ts, 'scan')
                exec_wf.connect(reg_ts, 'out_file',
                                mdl_wf, 'input_spec.time_series')
            elif self.registration_resource:
                # Merge the realigned images to 4D.
                reg_ts_rsc = self.registration_resource + '_ts'
                merge_reg = pe.Node(MergeNifti(out_format=reg_ts_rsc),
                                    name='merge_reg')

                # If the registration resource name was specified,
                # then download the previously realigned images.
                if reg_rsc:
                    reg_dl_xfc = XNATDownload(project=self.project,
                                              resource=reg_rsc)
                    download_reg = pe.Node(reg_dl_xfc,
                                           name='download_realigned_images')
                    exec_wf.connect(input_spec, 'subject',
                                    download_reg, 'subject')
                    exec_wf.connect(input_spec, 'session',
                                    download_reg, 'session')
                    exec_wf.connect(input_spec, 'scan',
                                    download_reg, 'scan')
                    if reg_node:
                        # Merge the previously and newly realigned images.
                        concat_reg = pe.Node(Merge(2),
                                             run_without_submitting=True,
                                             name='concat_reg')
                        exec_wf.connect(download_reg, 'out_files',
                                        concat_reg, 'in1')
                        exec_wf.connect(reg_node, 'out_files',
                                        concat_reg, 'in2')
                        exec_wf.connect(concat_reg, 'out',
                                        merge_reg, 'in_files')
                    else:
                        # All of the realigned files were downloaded.
                        exec_wf.connect(download_reg, 'out_files',
                                        merge_reg, 'in_files')
                elif reg_node:
                    # All of the realigned files were created by the
                    # registration workflow.
                    exec_wf.connect(reg_node, 'out_files',
                                    merge_reg, 'in_files')
                else:
                    raise ArgumentError(
                        "The QIN pipeline cannot perform modeling on the"
                        " registration result, since the registration"
                        " workflow is disabled and no registration resource"
                        " was specified.")

                # Upload the realigned time series to XNAT.
                upload_reg_ts_xfc = XNATUpload(project=self.project,
                                               resource=reg_ts_rsc,
                                               modality='MR')
                upload_reg_ts = pe.Node(upload_reg_ts_xfc,
                                        name='upload_reg_time_series')
                exec_wf.connect(input_spec, 'subject',
                                upload_reg_ts, 'subject')
                exec_wf.connect(input_spec, 'session',
                                upload_reg_ts, 'session')
                exec_wf.connect(input_spec, 'scan',
                                upload_reg_ts, 'scan')
                exec_wf.connect(merge_reg, 'out_file',
                                upload_reg_ts, 'in_files')

                # Pass the realigned time series to modeling.
                exec_wf.connect(merge_reg, 'out_file',
                                mdl_wf, 'input_spec.time_series')
                self._logger.debug('Connected registration to modeling.')
            else:
                # Model the scan input.
                exec_wf.connect(scan_ts, 'out_file',
                                mdl_wf, 'input_spec.time_series')

        # Set the configured workflow node inputs and plug-in options.
        self._configure_nodes(exec_wf)

        self._logger.debug("Created the %s workflow." % exec_wf.name)
        # If debug is set, then diagram the workflow graph.
        if self._logger.level <= logging.DEBUG:
            self.depict_workflow(exec_wf)

        return exec_wf

    def _run_workflow(self, workflow):
        """
        Overrides the superclass method to build the workflow if the
        *dry_run* instance variable flag is set.

        :param workflow: the workflow to run
        """
        super(QIPipelineWorkflow, self)._run_workflow(workflow)
        if self.dry_run:
            # Make a dummy empty file for simulating called workflows.
            _, path = tempfile.mkstemp()
            try:
                # If registration is enabled, then simulate it.
                if self.workflow.get_node('register'):
                    opts = dict(base_dir=self.workflow.base_dir, dry_run=True)
                    register('Dummy', 'Dummy', 'Dummy', 1, 0, path, [path], opts)
                # If ROI is enabled, then simulate it.
                if self.workflow.get_node('roi'):
                    opts = dict(base_dir=self.workflow.base_dir, dry_run=True)
                    # A dummy (lesion, slice index, in_file) ROI input tuple.
                    inputs = [(1, 1, path)]
                    roi('Dummy', 'Dummy', 'Dummy', 1, path, inputs, opts)
            finally:
                os.remove(path)


def bolus_arrival_index_or_zero(time_series):
    from qipipe.helpers.bolus_arrival import (bolus_arrival_index,
                                              BolusArrivalError)

    # Determines the bolus uptake. If it could not be determined,
    # then the first series is taken to be the uptake.
    try:
        return bolus_arrival_index(time_series)
    except BolusArrivalError:
        return 0


def register(project, subject, session, scan, bolus_arrival_index,
             mask, in_files, opts):
    """
    Runs the registration workflow on the given session scan images.

    :Note: contrary to Python convention, the opts method parameter
      is a required dictionary rather than a keyword aggregate (i.e.,
      ``**opts``). The Nipype ``Function`` interface does not support
      method aggregates. Similarly, the in_files parameter is a
      required list rather than a splat argument (i.e., *in_files).
    
    :param project: the project name
    :param subject: the subject name
    :param session: the session name
    :param scan: the scan number
    :param bolus_arrival_index: the bolus uptake volume index
    :param mask: the required scan mask file
    :param in_files: the input session scan 3D NiFTI images
    :param opts: the :meth:`qipipe.pipeline.registration.run` keyword
        options
    :return: the realigned image file path array
    """
    from qipipe.pipeline import registration

    # Note: There is always a mask argument. The mask file is either
    # specified as an input or built by the workflow. The mask is
    # optional in the registration run function. Therefore, the
    # the registration run options include the mask.
    run_opts = dict(mask=mask)
    run_opts.update(opts) 
    
    return registration.run(project, subject, session, scan,
                            bolus_arrival_index, *in_files, **run_opts)


def roi(project, subject, session, scan, time_series, in_rois, opts):
    """
    Runs the ROI workflow on the given session scan images.

    :Note: see the :meth:`register` note.

    :param project: the project name
    :param subject: the subject name
    :param session: the session name
    :param scan: the scan number
    :param time_series: the scan 4D time series
    :param in_rois: the :meth:`qipipe.pipeline.roi.run` input tuples
    :param opts: the :meth:`qipipe.pipeline.roi.run` keyword options
    """
    from qipipe.pipeline import roi

    roi.run(project, subject, session, scan, time_series, *in_rois, **opts)
