from rtcclient.base import RTCBase
import xmltodict
from rtcclient import exception
from rtcclient.project_area import ProjectArea, TeamArea, Member, Administrator
from rtcclient.project_area import PlannedFor, FiledAgainst, FoundIn
from rtcclient.project_area import Severity, Priority, ItemType
from rtcclient.workitem import Workitem, Comment, Action
import logging
from rtcclient import urlparse, urlquote, urlencode, OrderedDict
import copy
from rtcclient.template import Templater
from rtcclient import _search_path
from rtcclient.query import Query
# import urlparse


class RTCClient(RTCBase):
    """A wrapped class for RTC Client

    Tips: You can also customize your preferred properties to be returned
    by specified `returned_properties` when the called methods contain
    this optional parameter, which can also GREATLY IMPROVE the performance
    of this client especially when getting and querying lots of Workitems.

    Important Note: `returned_properties` is an advanced parameter, the
    returned properties can be found in `ClassInstance.field_alias.values()`,
    e.g. `myworkitem1.field_alias.values()`. If you don't care the performance,
    just leave it alone with None.
    """

    log = logging.getLogger("client.RTCClient")

    def __init__(self, url, username, password, searchpath=_search_path):
        """Initialization

        :param url: the rtc url (example: https://your_domain:9443/jazz)
        :param username: the rtc username
        :param password: the rtc password
        :param searchpath: the folder to store your templates
        """

        self.username = username
        self.password = password
        RTCBase.__init__(self, url)
        self.headers = self._get_headers()
        self.templater = Templater(self, searchpath=searchpath)
        self.query = Query(self)

    def __str__(self):
        return "RTC Server at %s" % self.url

    def get_rtc_obj(self):
        return self

    def _get_headers(self):
        # TODO: for invalid username or password,
        _headers = {"Content-Type": self.CONTENT_XML}
        resp = self.get(self.url + "/authenticated/identity",
                        verify=False,
                        headers=_headers)

        _headers["Content-Type"] = self.CONTENT_URL_ENCODED
        _headers["Cookie"] = resp.headers.get("set-cookie")
        credentials = urlencode({"j_username": self.username,
                                 "j_password": self.password})

        resp = self.post(self.url + "/authenticated/j_security_check",
                         data=credentials,
                         verify=False,
                         headers=_headers)

        resp = self.get(self.url + "/authenticated/identity",
                        verify=False,
                        headers=_headers)

        _headers["Cookie"] = resp.headers.get("set-cookie")
        _headers["Accept"] = self.CONTENT_XML
        return _headers

    def getProjectAreas(self, archived=False,
                        returned_properties=None):
        """Get all <ProjectArea> objects

        If no ProjectAreas are retrieved, None is returned.

        :param archived: whether the ProjectAreas are archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: A list contains all the <ProjectArea> objects
        :rtype: list
        """

        rp = returned_properties
        return self._get_paged_resources("ProjectArea",
                                         page_size="10",
                                         archived=archived,
                                         returned_properties=rp)

    def getProjectArea(self, projectarea_name, archived=False,
                       returned_properties=None):
        """Get <ProjectArea> object by its name

        :param archived: whether the ProjectArea is archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :param projectarea_name: the project area name
        :return: :class:`ProjectArea <ProjectArea>` object
        :rtype: project_area.ProjectArea
        """

        self.log.debug("Try to get <ProjectArea %s>", projectarea_name)
        if not isinstance(projectarea_name, str) or not projectarea_name:
            excp_msg = "Please specify a valid ProjectArea name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        rp = returned_properties
        proj_areas = self.getProjectAreas(archived=archived,
                                          returned_properties=rp)
        if proj_areas is not None:
            for proj_area in proj_areas:
                if proj_area.title == projectarea_name:
                    self.log.info("Find <ProjectArea %s>", proj_area)
                    return proj_area

        self.log.error("No ProjectArea named %s", projectarea_name)
        raise exception.NotFound("No ProjectArea named %s" % projectarea_name)

    def getProjectAreaByID(self, projectarea_id, archived=False,
                           returned_properties=None):
        """Get <ProjectArea> object by its id

        :param projectarea_id: the project area id
        :param archived: whether the ProjectArea is archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: :class:`ProjectArea <ProjectArea>` object
        :rtype: project_area.ProjectArea
        """

        self.log.debug("Try to get <ProjectArea> by its id: %s",
                       projectarea_id)
        if not isinstance(projectarea_id, str) or not projectarea_id:
            excp_msg = "Please specify a valid ProjectArea ID"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        rp = returned_properties
        proj_areas = self.getProjectAreas(archived=archived,
                                          returned_properties=rp)
        if proj_areas is not None:
            for proj_area in proj_areas:
                if proj_area.id == projectarea_id:
                    self.log.info("Find <ProjectArea %s>", proj_area)
                    return proj_area

        self.log.error("No ProjectArea's ID is %s", projectarea_id)
        raise exception.NotFound("No ProjectArea's ID is %s" % projectarea_id)

    def getProjectAreaID(self, projectarea_name, archived=False):
        """Get <ProjectArea> id by projectarea name

        :param projectarea_name: the project area name
        :param archived: whether the ProjectArea is archived
        :return :class `string` object
        :rtype: string
        """

        self.log.debug("Get the ProjectArea id by its name: %s",
                       projectarea_name)
        proj_area = self.getProjectArea(projectarea_name,
                                        archived=archived)
        if proj_area:
            return proj_area.id
        raise exception.NotFound("No ProjectArea named %s" % projectarea_name)

    def getProjectAreaIDs(self, projectarea_name=None, archived=False):
        """Get all <ProjectArea> ID(s) by projectarea name

        If `projectarea_name` is None, all the ProjectArea IDs
        will be returned.

        :param projectarea_name: the project area name
        :param archived: whether the ProjectAreas are archived
        :return: a list contains all the ProjectArea IDs
        :rtype: list
        """

        projectarea_ids = list()
        if projectarea_name and isinstance(projectarea_name, str):
            projectarea_id = self.getProjectAreaID(projectarea_name,
                                                   archived=archived)
            projectarea_ids.append(projectarea_id)
        elif projectarea_name is None:
            projectareas = self.getProjectAreas(archived=archived)
            if projectareas is None:
                return None
            projectarea_ids = [proj_area.id for proj_area in projectareas]
        else:
            error_msg = "Invalid ProjectArea name: [%s]" % projectarea_name
            self.log.error(error_msg)
            raise exception.BadValue(error_msg)

        return projectarea_ids

    def checkProjectAreaID(self, projectarea_id, archived=False):
        """Check the validity of <ProjectArea> ID

        :param projectarea_id: the project area id
        :param archived: whether the ProjectArea is archived
        :return True or False
        :rtype: bool
        """

        self.log.debug("Check the validity of the ProjectArea id: %s",
                       projectarea_id)

        proj_areas = self.getProjectAreas(archived=archived)
        if proj_areas is not None:
            for proj_area in proj_areas:
                if proj_area.id == projectarea_id:
                    self.log.info("Find <ProjectArea %s> whose id is: %s",
                                  proj_area,
                                  projectarea_id)
                    return True

        self.log.error("No ProjectArea whose id is: %s",
                       projectarea_id)
        return False

    def getTeamArea(self, teamarea_name, projectarea_id=None,
                    projectarea_name=None, archived=False,
                    returned_properties=None):
        """Get <TeamArea> object by TeamArea name

        If ProjectArea id or name is specified, then the matched TeamArea in
        that ProjectArea will be returned.
        Otherwise, return the first found TeamArea with that name.

        :param teamarea_name: the TeamArea name
        :param projectarea_id: the ProjectArea id
        :param projectarea_name: the ProjectArea name
        :param archived: whether the TeamArea is archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: the `TeamArea <TeamArea>` object
        :rtype: projectarea.TeamArea
        """

        self.log.debug("Try to get <TeamArea %s>", teamarea_name)
        if not isinstance(teamarea_name, str) or not teamarea_name:
            excp_msg = "Please specify a valid TeamArea name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        teamareas = self.getTeamAreas(projectarea_id=projectarea_id,
                                      projectarea_name=projectarea_name,
                                      archived=archived,
                                      returned_properties=returned_properties)

        if teamareas is not None:
            for teamarea in teamareas:
                # TODO: check the title uniqueness
                if teamarea.title == teamarea_name:
                    self.log.info("Find <TeamArea %s>", teamarea)
                    return teamarea

        self.log.error("No TeamArea named %s", teamarea_name)
        raise exception.NotFound("No TeamArea named %s" % teamarea_name)

    def getTeamAreas(self, projectarea_id=None, projectarea_name=None,
                     archived=False, returned_properties=None):
        """Get all <TeamArea> objects by projectarea's id or name

        If both `projectarea_id` and `projectarea_name` are None,
        all the TeamAreas in all ProjectAreas will be returned.

        If no TeamAreas are retrieved, None is returned.

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the TeamAreas are archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: a list contains all the `TeamArea <TeamArea>` objects
        :rtype: list
        """

        projarea_id = self._pre_get_resource(projectarea_id=projectarea_id,
                                             projectarea_name=projectarea_name)

        rp = returned_properties
        return self._get_paged_resources("TeamArea",
                                         projectarea_id=projarea_id,
                                         page_size="100",
                                         archived=archived,
                                         returned_properties=rp)

    def getOwnedBy(self, email, projectarea_id=None,
                   projectarea_name=None):

        if not isinstance(email, str) or "@" not in email:
            excp_msg = "Please specify a valid email address name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        parse_result = urlparse.urlparse(self.url)
        new_path = "/".join(["/jts/users",
                             urlquote(email)])
        new_parse_result = urlparse.ParseResult(scheme=parse_result.scheme,
                                                netloc=parse_result.netloc,
                                                path=new_path,
                                                params=parse_result.params,
                                                query=parse_result.query,
                                                fragment=parse_result.fragment)
        return Member(urlparse.urlunparse(new_parse_result),
                      self)

    def getPlannedFor(self, plannedfor_name, projectarea_id=None,
                      projectarea_name=None, archived=False,
                      returned_properties=None):
        """Get <PlannedFor> object by PlannedFor name

        :param plannedfor_name: the PlannedFor name
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the PlannedFor is archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: the `PlannedFor <PlannedFor>` object
        :rtype: projectarea.PlannedFor
        """

        self.log.debug("Try to get <PlannedFor %s>", plannedfor_name)
        if not isinstance(plannedfor_name, str) or not plannedfor_name:
            excp_msg = "Please specify a valid PlannedFor name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        rp = returned_properties
        plannedfors = self.getPlannedFors(projectarea_id=projectarea_id,
                                          projectarea_name=projectarea_name,
                                          archived=archived,
                                          returned_properties=rp)

        if plannedfors is not None:
            for plannedfor in plannedfors:
                if plannedfor.title == plannedfor_name:
                    self.log.info("Find <PlannedFor %s>", plannedfor)
                    return plannedfor

        self.log.error("No PlannedFor named %s", plannedfor_name)
        raise exception.NotFound("No PlannedFor named %s" % plannedfor_name)

    def getPlannedFors(self, projectarea_id=None, projectarea_name=None,
                       archived=False, returned_properties=None):
        """Get all <PlannedFor> objects by projectarea's id or name

        If both `projectarea_id` and `projectarea_name` are None,
        all the PlannedFors in all ProjectAreas will be returned.

        If no PlannedFors are retrieved, None is returned.

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the PlannedFors are archived
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: a list contains all the `PlannedFor <PlannedFor>` objects
        :rtype: list
        """

        projarea_id = self._pre_get_resource(projectarea_id=projectarea_id,
                                             projectarea_name=projectarea_name)

        rp = returned_properties
        return self._get_paged_resources("PlannedFor",
                                         projectarea_id=projarea_id,
                                         page_size="100",
                                         archived=archived,
                                         returned_properties=rp)

    def getSeverity(self, severity_name, projectarea_id=None,
                    projectarea_name=None):
        """Get <Severity> object by Severity name

        At least either of `projectarea_id` and `projectarea_name` is given

        :param severity_name: the Severity name
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :return: the `Severity <Severity>` object
        :rtype: projectarea.Severity
        """

        self.log.debug("Try to get <Severity %s>", severity_name)
        if not isinstance(severity_name, str) or not severity_name:
            excp_msg = "Please specify a valid Severity name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        severities = self.getSeverities(projectarea_id=projectarea_id,
                                        projectarea_name=projectarea_name)

        if severities is not None:
            for severity in severities:
                if severity.title == severity_name:
                    self.log.info("Find <Severity %s>", severity)
                    return severity

        self.log.error("No Severity named %s", severity_name)
        raise exception.NotFound("No Severity named %s" % severity_name)

    def getSeverities(self, projectarea_id=None, projectarea_name=None):
        """Get all <Severity> objects by projectarea's id or name

        At least either of `projectarea_id` and `projectarea_name` is given

        If no Severities are retrieved, None is returned.

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :return: a list contains all the `Severity <Severity>` objects
        :rtype: list
        """

        projarea_id = self._pre_get_resource(projectarea_id=projectarea_id,
                                             projectarea_name=projectarea_name)
        if projarea_id is None:
            self.log.error("Please input either-or between "
                           "projectarea_id and projectarea_name")
            raise exception.EmptyAttrib("At least input either-or between "
                                        "projectarea_id and projectarea_name")
        return self._get_paged_resources("Severity",
                                         projectarea_id=projarea_id,
                                         page_size="10")

    def getPriority(self, priority_name, projectarea_id=None,
                    projectarea_name=None):
        """Get <Priority> object by Priority name

        At least either of `projectarea_id` and `projectarea_name` is given

        :param priority_name: the Priority name
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :return: the `Priority <Priority>` object
        :rtype: projectarea.Priority
        """

        self.log.debug("Try to get <Priority %s>", priority_name)
        if not isinstance(priority_name, str) or not priority_name:
            excp_msg = "Please specify a valid Priority name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        priorities = self.getPriorities(projectarea_id=projectarea_id,
                                        projectarea_name=projectarea_name)

        if priorities is not None:
            for priority in priorities:
                if priority.title == priority_name:
                    self.log.info("Find <Priority %s>", priority)
                    return priority

        self.log.error("No Priority named %s", priority_name)
        raise exception.NotFound("No Priority named %s" % priority_name)

    def getPriorities(self, projectarea_id=None, projectarea_name=None):
        """Get all <Priority> objects by projectarea's id or name

        At least either of `projectarea_id` and `projectarea_name` is given.

        If no Priorities are retrieved, None is returned.

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :return: a list contains all the `Priority <Priority>` objects
        :rtype: list
        """

        projarea_id = self._pre_get_resource(projectarea_id=projectarea_id,
                                             projectarea_name=projectarea_name)
        if projarea_id is None:
            self.log.error("Please input either-or between "
                           "projectarea_id and projectarea_name")
            raise exception.EmptyAttrib("At least input either-or between "
                                        "projectarea_id and projectarea_name")
        return self._get_paged_resources("Priority",
                                         projectarea_id=projarea_id,
                                         page_size="10")

    def getFoundIn(self, foundin_name, projectarea_id=None,
                   projectarea_name=None, archived=False):
        """Get <FoundIn> object by FoundIn name

        :param foundin_name: the FoundIn name
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the FoundIn is archived
        :return: the `FoundIn <FoundIn>` object
        :rtype: projectarea.FoundIn
        """

        self.log.debug("Try to get <FoundIn %s>", foundin_name)
        if not isinstance(foundin_name, str) or not foundin_name:
            excp_msg = "Please specify a valid PlannedFor name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        foundins = self.getFoundIns(projectarea_id=projectarea_id,
                                    projectarea_name=projectarea_name,
                                    archived=archived)

        if foundins is not None:
            for foundin in foundins:
                if foundin.title == foundin_name:
                    self.log.info("Find <FoundIn %s>", foundin)
                    return foundin

        self.log.error("No FoundIn named %s", foundin_name)
        raise exception.NotFound("No FoundIn named %s" % foundin_name)

    def getFoundIns(self, projectarea_id=None, projectarea_name=None,
                    archived=False):
        """Get all <FoundIn> objects by projectarea's id or name

        If both `projectarea_id` and `projectarea_name` are None,
        all the FoundIns in all ProjectAreas will be returned.

        If no FoundIns are retrieved, None is returned.

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the FoundIns are archived
        :return: a list contains all the `FoundIn <FoundIn>` objects
        :rtype: list
        """

        projarea_id = self._pre_get_resource(projectarea_id=projectarea_id,
                                             projectarea_name=projectarea_name)
        return self._get_paged_resources("FoundIn",
                                         projectarea_id=projarea_id,
                                         page_size="100",
                                         archived=archived)

    def getFiledAgainst(self, filedagainst_name, projectarea_id=None,
                        projectarea_name=None, archived=False):
        """Get <FiledAgainst> object by FiledAgainst name

        :param filedagainst_name: the FiledAgainst name
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the FiledAgainst is archived
        :return: the `FiledAgainst <FiledAgainst>` object
        :rtype: projectarea.FiledAgainst
        """

        self.log.debug("Try to get <FiledAgainst %s>", filedagainst_name)
        if not isinstance(filedagainst_name, str) or not filedagainst_name:
            excp_msg = "Please specify a valid FiledAgainst name"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)

        fas = self.getFiledAgainsts(projectarea_id=projectarea_id,
                                    projectarea_name=projectarea_name,
                                    archived=archived)

        if fas is not None:
            for filedagainst in fas:
                if filedagainst.title == filedagainst_name:
                    self.log.info("Find <FiledAgainst %s>", filedagainst)
                    return filedagainst

        error_msg = "No FiledAgainst named %s" % filedagainst_name
        self.log.error(error_msg)
        raise exception.NotFound(error_msg)

    def getFiledAgainsts(self, projectarea_id=None, projectarea_name=None,
                         archived=False):
        """Get all <FiledAgainst> objects by projectarea's id or name

        If both `projectarea_id` and `projectarea_name` are None,
        all the FiledAgainsts in all ProjectAreas will be returned.

        If no FiledAgainsts are retrieved, None is returned.

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param archived: whether the FiledAgainsts are archived
        :return: a list contains all the `FiledAgainst <FiledAgainst>` objects
        :rtype: list
        """

        projarea_id = self._pre_get_resource(projectarea_id=projectarea_id,
                                             projectarea_name=projectarea_name)
        return self._get_paged_resources("FiledAgainst",
                                         projectarea_id=projarea_id,
                                         page_size="100",
                                         archived=archived)

    def getTemplate(self, copied_from, template_name=None,
                    template_folder=None, keep=False, encoding="UTF-8"):
        """Get template from some to-be-copied workitem

        More detals, please refer to `Templater.getTemplate`
        """

        return self.templater.getTemplate(copied_from,
                                          template_name=template_name,
                                          template_folder=template_folder,
                                          keep=keep,
                                          encoding=encoding)

    def getTemplates(self, workitems, template_folder=None,
                     template_names=None, keep=False, encoding="UTF-8"):
        """Get templates from a group of to-be-copied workitems and write
        them to files named after the names in `template_names` respectively.

        More detals, please refer to `Templater.getTemplate`
        """

        self.templater.getTemplates(workitems,
                                    template_folder=template_folder,
                                    template_names=template_names,
                                    keep=keep,
                                    encoding=encoding)

    def listFields(self, template):
        """List all the attributes to be rendered from the template file

        :param template: The template to render.
            The template is actually a file, which is usually generated
            by `Template.getTemplate()` and can also be modified by user
            accordingly.
        :return: a set contains all the needed attributes
        :rtype: set

        More detals, please refer to `Templater.listFieldsFromWorkitem`
        """

        return self.templater.listFields(template)

    def listFieldsFromWorkitem(self, copied_from, keep=False):
        """List all the attributes to be rendered directly from some
        to-be-copied workitem

        More detals, please refer to `Templater.listFieldsFromWorkitem`
        """

        return self.templater.listFieldsFromWorkitem(copied_from,
                                                     keep=keep)

    def getWorkitem(self, workitem_id, returned_properties=None):
        """Get <Workitem> object by its id/number

        :param workitem_id: the workitem number (integer or string)
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :return: :class:`Workitem <Workitem>` object
        :rtype: workitem.Workitem
        """

        try:
            if isinstance(workitem_id, bool):
                raise ValueError()
            if isinstance(workitem_id, str):
                workitem_id = int(workitem_id)
            if not isinstance(workitem_id, int):
                raise ValueError()

            workitem_url = "/".join([self.url,
                                     "oslc/workitems/%s" % workitem_id])
            if returned_properties is not None:
                workitem_url = "".join([workitem_url,
                                        "?oslc_cm.properties=",
                                        urlquote(returned_properties)])
            resp = self.get(workitem_url,
                            verify=False,
                            headers=self.headers)
            raw_data = xmltodict.parse(resp.content)
            workitem_raw = raw_data["oslc_cm:ChangeRequest"]

            return Workitem(workitem_url,
                            self,
                            workitem_id=workitem_id,
                            raw_data=workitem_raw)

        except ValueError:
            excp_msg = "Please input a valid workitem id"
            self.log.error(excp_msg)
            raise exception.BadValue(excp_msg)
        except Exception, excp:
            self.log.error(excp)
            raise exception.NotFound("Not found <Workitem %s>", workitem_id)

    def getWorkitems(self, projectarea_id=None, projectarea_name=None,
                     returned_properties=None, archived=False):
        """Get all <Workitem> objects by projectarea's id or name

        If both projectarea_id and projectarea_name are None, all the workitems
        in all ProjectAreas will be returned.

        If no Workitems are retrieved, None is returned.

        You can also customize your preferred properties to be returned
        by specified `returned_properties`

        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :param archived: whether the Workitems are archived
        :return: a list contains all the `Workitem <Workitem>` objects
        :rtype: list
        """

        workitems_list = list()
        projectarea_ids = list()
        if not isinstance(projectarea_id, str) or not projectarea_id:
            pa_ids = self.getProjectAreaIDs(projectarea_name)
            if pa_ids is None:
                self.log.warning("Stop getting workitems because of "
                                 "no ProjectAreas")
                return None
            projectarea_ids.extend(pa_ids)
        else:
            if self.checkProjectAreaID(projectarea_id):
                projectarea_ids.append(projectarea_id)
            else:
                raise exception.BadValue("Invalid ProjectAred ID: "
                                         "%s" % projectarea_id)

        self.log.warning("For a single ProjectArea, only latest 1000 "
                         "workitems can be fetched. "
                         "This may be a bug of Rational Team Concert")

        rp = returned_properties
        for projarea_id in projectarea_ids:
            workitems = self._get_paged_resources("Workitem",
                                                  projectarea_id=projarea_id,
                                                  page_size="100",
                                                  returned_properties=rp,
                                                  archived=archived)
            if workitems is not None:
                workitems_list.extend(workitems)

        if not workitems_list:
            self.log.warning("Cannot find a workitem in the ProjectAreas "
                             "with ids: %s" % projectarea_ids)
            return None
        return workitems_list

    def createWorkitem(self, item_type, title, description=None,
                       projectarea_id=None, projectarea_name=None,
                       template=None, copied_from=None, keep=False,
                       **kwargs):
        """Create a workitem

        :param item_type: the type of the workitem (e.g. task/defect/issue)
        :param title: the title of the new created workitem
        :param description: the description of the new created workitem
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param template: The template to render.
            The template is actually a file, which is usually generated
            by `Template.getTemplate()` and can also be modified by user
            accordingly.
        :param copied_from: the to-be-copied workitem id
        :param keep: refer to `keep` in `Templater.getTemplate`
            only works when `template` is not specified
        :param \*\*kwargs: Optional/mandatory arguments when creating a new
            workitem. More details, please refer to `kwargs` in
            `Templater.render`
        :return: :class:`Workitem <Workitem>` object
        :rtype: workitem.Workitem
        """

        if not isinstance(projectarea_id, str) or not projectarea_id:
            projectarea = self.getProjectArea(projectarea_name)
            projectarea_id = projectarea.id
        else:
            projectarea = self.getProjectAreaByID(projectarea_id)

        itemtype = projectarea.getItemType(item_type)

        if not template:
            if not copied_from:
                self.log.error("Please choose either-or between "
                               "template and copied_from")
                raise exception.EmptyAttrib("At least choose either-or "
                                            "between template and copied_from")

            self._checkMissingParamsFromWorkitem(copied_from, keep=keep,
                                                 **kwargs)
            kwargs = self._retrieveValidInfo(projectarea_id,
                                             **kwargs)
            wi_raw = self.templater.renderFromWorkitem(copied_from,
                                                       keep=keep,
                                                       encoding="UTF-8",
                                                       title=title,
                                                       description=description,
                                                       **kwargs)

        else:
            self._checkMissingParams(template, **kwargs)
            kwargs = self._retrieveValidInfo(projectarea_id,
                                             **kwargs)
            wi_raw = self.templater.render(template,
                                           title=title,
                                           description=description,
                                           **kwargs)

        self.log.info("Start to create a new <%s> with raw data: %s",
                      item_type, wi_raw)

        wi_url_post = "/".join([self.url,
                                "/oslc/contexts",
                                projectarea_id,
                                "workitems/%s" % itemtype.identifier])
        return self._createWorkitem(wi_url_post, wi_raw)

    def copyWorkitem(self, copied_from, title=None, description=None,
                     prefix=None):
        """Create a workitem by copying from an existing one

        :param copied_from: the to-be-copied workitem id
        :param title: the new workitem title.
            If None, will copy that from to-be-copied workitem
        :param description: the new workitem description.
            If None, will copy that from to-be-copied workitem
        :param prefix: used to add a prefix to the copied title and
            description
        """

        copied_wi = self.getWorkitem(copied_from)
        if title is None:
            title = copied_wi.title
            if prefix is not None:
                title = prefix + title

        if description is None:
            description = copied_wi.description
            if prefix is not None:
                description = prefix + description

        self.log.info("Start to create a new <Workitem>, copied from ",
                      "<Workitem %s>", copied_from)

        wi_url_post = "/".join([self.url,
                                "oslc/contexts/%s" % copied_wi.contextId,
                                "workitems",
                                "%s" % copied_wi.type.split("/")[-1]])
        wi_raw = self.templater.renderFromWorkitem(copied_from,
                                                   keep=True,
                                                   encoding="UTF-8",
                                                   title=title,
                                                   description=description)
        return self._createWorkitem(wi_url_post, wi_raw)

    def _createWorkitem(self, url_post, workitem_raw):
        headers = copy.deepcopy(self.headers)
        headers['Content-Type'] = self.OSLC_CR_XML

        resp = self.post(url_post, verify=False,
                         headers=headers, data=workitem_raw)

        raw_data = xmltodict.parse(resp.content)
        workitem_raw = raw_data["oslc_cm:ChangeRequest"]
        workitem_id = workitem_raw["dc:identifier"]
        workitem_url = "/".join([self.url,
                                 "oslc/workitems/%s" % workitem_id])
        new_wi = Workitem(workitem_url,
                          self,
                          workitem_id=workitem_id,
                          raw_data=raw_data["oslc_cm:ChangeRequest"])

        self.log.info("Successfully create <Workitem %s>" % new_wi)
        return new_wi

    def _checkMissingParams(self, template, **kwargs):
        """Check the missing parameters for rendering from the template file
        """

        parameters = self.listFields(template)
        self._findMissingParams(parameters, **kwargs)

    def _checkMissingParamsFromWorkitem(self, copied_from, keep=False,
                                        **kwargs):
        """Check the missing parameters for rendering directly from the
        copied workitem
        """

        parameters = self.listFieldsFromWorkitem(copied_from,
                                                 keep=keep)
        self._findMissingParams(parameters, **kwargs)

    def _retrieveValidInfo(self, projectarea_id, **kwargs):
        # get rdf:resource by keywords
        for keyword in kwargs.keys():
            try:
                keyword_cls = eval("self.get" + keyword.capitalize())
                keyword_obj = keyword_cls(kwargs[keyword],
                                          projectarea_id=projectarea_id)
                kwargs[keyword] = keyword_obj.url
            except Exception, excp:
                self.log.error(excp)
        return kwargs

    def _findMissingParams(self, parameters, **kwargs):
        known_parameters = ["title", "description"]
        for known_parameter in known_parameters:
            try:
                parameters.remove(known_parameter)
            except KeyError:
                continue

        input_attributes = set(kwargs.keys())
        missing_attributes = parameters.difference(input_attributes)
        if not missing_attributes:
            error_msg = "Missing Parameters: %s" % list(missing_attributes)
            self.log.error(error_msg)
            raise exception.EmptyAttrib(error_msg)
        else:
            self.log.debug("No missing parameters")

    def checkType(self, item_type, projectarea_id):
        """Check the validity of workitem type

        :param item_type: the type of the workitem (e.g. Story/Defect/Epic)
        :param projectarea_id: the project area id
        :return: True or False
        :rtype: bool
        """

        self.log.debug("Checking the validity of workitem type: %s",
                       item_type)
        try:
            project_area = self.getProjectAreaByID(projectarea_id)
            if project_area.getItemType(item_type):
                return True
            else:
                return False
        except (exception.NotFound, exception.BadValue):
            self.log.error("Invalid ProjectArea name")
            return False

    def _pre_get_resource(self, projectarea_id=None, projectarea_name=None):
        if projectarea_id is None:
            if projectarea_name is not None:
                return self.getProjectAreaID(projectarea_name)
            return None
        else:
            if not self.checkProjectAreaID(projectarea_id):
                raise exception.BadValue("Invalid ProjectArea id")
            return projectarea_id

    def _get_paged_resources(self, resource_name, projectarea_id=None,
                             workitem_id=None, customized_attr=None,
                             page_size="100", archived=False,
                             returned_properties=None):
        # TODO: multi-thread

        self.log.debug("Start to fetch all %ss with [ProjectArea ID: %s] "
                       "and [archived=%s]",
                       resource_name,
                       projectarea_id if projectarea_id else "not specified",
                       archived)

        projectarea_required = ["Workitem",
                                "Severity",
                                "Priority",
                                "Member",
                                "Administrator",
                                "ItemType",
                                "Action",
                                "Query"]
        workitem_required = ["Comment",
                             "Subscriber"]
        customized_required = ["Action",
                               "Query"]

        if resource_name in projectarea_required and not projectarea_id:
            self.log.error("No ProjectArea ID is specified")
            raise exception.EmptyAttrib("No ProjectArea ID")

        if resource_name in workitem_required and not workitem_id:
            self.log.error("No Workitem ID is specified")
            raise exception.EmptyAttrib("No Workitem ID")

        if resource_name in customized_required and not customized_attr:
            self.log.error("No customized value is specified")
            raise exception.EmptyAttrib("No customized value")

        res_map = {"TeamArea": "teamareas",
                   "ProjectArea": "projectareas",
                   "FiledAgainst": "categories",
                   "FoundIn": "deliverables",
                   "PlannedFor": "iterations",
                   "ItemType": "types/%s" % projectarea_id,
                   "Member": "projectareas/%s/rtc_cm:members" % projectarea_id,
                   "Administrator": "/".join(["projectareas",
                                              "%s" % projectarea_id,
                                              "rtc_cm:administrators"]),
                   "Workitem": "contexts/%s/workitems" % projectarea_id,
                   "Severity": "enumerations/%s/severity" % projectarea_id,
                   "Priority": "enumerations/%s/priority" % projectarea_id,
                   "Comment": "workitems/%s/rtc_cm:comments" % workitem_id,
                   "Subscriber": "/".join(["workitems",
                                           "%s" % workitem_id,
                                           "rtc_cm:subscribers"]),
                   "Action": "workflows/%s/actions/%s" % (projectarea_id,
                                                          customized_attr),
                   "Query": "".join(["contexts/%s/workitems" % projectarea_id,
                                     "?oslc_cm.query=%s" % customized_attr])
                   }

        entry_map = {"TeamArea": "rtc_cm:Team",
                     "ProjectArea": "rtc_cm:Project",
                     "FiledAgainst": "rtc_cm:Category",
                     "FoundIn": "rtc_cm:Deliverable",
                     "PlannedFor": "rtc_cm:Iteration",
                     "ItemType": "rtc_cm:Type",
                     "Member": "rtc_cm:User",
                     "Administrator": "rtc_cm:User",
                     "Workitem": "oslc_cm:ChangeRequest",
                     "Severity": "rtc_cm:Literal",
                     "Priority": "rtc_cm:Literal",
                     "Comment": "rtc_cm:Comment",
                     "Subscriber": "rtc_cm:User",
                     "Action": "rtc_cm:Action",
                     "Query": "oslc_cm:ChangeRequest"
                     }

        if resource_name not in res_map:
            self.log.error("Unsupported resource name")
            raise exception.BadValue("Unsupported resource name")

        resource_url = "".join([self.url,
                                "/oslc/{0}",
                                "?" if resource_name != "Query"
                                else "&",
                                "oslc_cm.pageSize={1}&_startIndex=0"])

        resource_url = resource_url.format(res_map[resource_name],
                                           page_size)

        if returned_properties is not None:
            if not isinstance(returned_properties, str):
                raise exception.BadValue("returned_properties is not a"
                                         "valid string")
            resource_url = "".join([resource_url,
                                    "&oslc_cm.properties=",
                                    urlquote(returned_properties)])

        pa_url = ("/".join([self.url,
                            "oslc/projectareas",
                            projectarea_id])
                  if projectarea_id else None)

        resp = self.get(resource_url,
                        verify=False,
                        headers=self.headers)
        raw_data = xmltodict.parse(resp.content)

        try:
            total_count = int(raw_data.get("oslc_cm:Collection")
                                      .get("@oslc_cm:totalCount"))
            if total_count == 0:
                self.log.warning("No %ss are found", resource_name)
                return None
        except:
            pass

        resources_list = []

        while True:
            entries = (raw_data.get("oslc_cm:Collection")
                               .get(entry_map[resource_name]))

            if entries is None:
                break

            # for the last single entry
            if isinstance(entries, OrderedDict):
                resource = self._handle_resource_entry(resource_name,
                                                       entries,
                                                       projectarea_url=pa_url,
                                                       archived=archived)
                if resource is not None:
                    resources_list.append(resource)
                break

            # iterate all the entries
            for entry in entries:
                resource = self._handle_resource_entry(resource_name,
                                                       entry,
                                                       projectarea_url=pa_url,
                                                       archived=archived)
                if resource is not None:
                    resources_list.append(resource)

            # find the next page
            url_next = raw_data.get('oslc_cm:Collection').get('@oslc_cm:next')
            if url_next:
                resp = self.get(url_next,
                                verify=False,
                                headers=self.headers)
                raw_data = xmltodict.parse(resp.content)
            else:
                break

        if not resources_list:
            self.log.warning("No %ss are found with [ProjectArea ID: %s] "
                             "and [archived=%s]",
                             resource_name,
                             projectarea_id if projectarea_id
                             else "not specified",
                             archived)
            return None

        self.log.debug("Successfully fetching all the paged resources")
        return resources_list

    def _handle_resource_entry(self, resource_name, entry,
                               projectarea_url=None, archived=False):
        if projectarea_url is not None:
            try:
                if (entry.get("rtc_cm:projectArea")
                         .get("@rdf:resource")) != projectarea_url:
                    return None
            except AttributeError:
                pass

        entry_archived = entry.get("rtc_cm:archived")
        if (entry_archived is not None and
                eval(entry_archived.capitalize()) != archived):
            return None

        if resource_name == "Subscriber":
            resource_cls = Member
        elif resource_name == "Query":
            resource_cls = Workitem
        else:
            resource_cls = eval(resource_name)

        if resource_name in ["Workitem",
                             "Query"]:
            resource_url = entry.get("@rdf:resource")
            resource_url = "/".join([self.url,
                                     "oslc/workitems",
                                     resource_url.split("/")[-1]])
        else:
            resource_url = entry.get("@rdf:resource")

        resource = resource_cls(resource_url,
                                self,
                                raw_data=entry)
        return resource

    def queryWorkitems(self, query_str, projectarea_id=None,
                       projectarea_name=None, returned_properties=None,
                       archived=False):
        """Query workitems with the query string in a certain ProjectArea

        At least either of `projectarea_id` and `projectarea_name` is given

        :param query_str: a valid query string
        :param projectarea_id: the project area id
        :param projectarea_name: the project area name
        :param returned_properties: the returned properties that you want
            Refer to class `RTCClient` for more explanations
        :param archived: whether the Workitems are archived
        :return: a list contains the queried <Workitem> objects
        :rtype: list
        """

        rp = returned_properties
        return self.query.queryWorkitems(query_str=query_str,
                                         projectarea_id=projectarea_id,
                                         projectarea_name=projectarea_name,
                                         returned_properties=rp,
                                         archived=archived)
