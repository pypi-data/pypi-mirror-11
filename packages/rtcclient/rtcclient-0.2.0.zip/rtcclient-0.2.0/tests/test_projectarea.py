import requests
import pytest
import utils_test
from rtcclient.project_area import ProjectArea
from rtcclient.models import Member, ItemType, Administrator, Role
from rtcclient.exception import BadValue, NotFound, EmptyAttrib


class TestProjectArea:
    @pytest.fixture(autouse=True)
    def myrtcclient(self, rtcclient):
        myclient = rtcclient
        return myclient

    def test_init_projectarea_exception(self, myrtcclient):
        pa_url = "/".join(["http://test.url:9443/jazz/oslc",
                           "projectareas/_0qMJUMfiEd6yW_0tvNlbrw"])
        with pytest.raises(EmptyAttrib):
            ProjectArea(pa_url, myrtcclient, raw_data=None)

    @pytest.fixture(autouse=True)
    def mypa(self, myrtcclient):
        pa_url = "/".join(["http://test.url:9443/jazz/oslc",
                           "projectareas/_CuZu0HUwEeKicpXBddtqNA"])
        return ProjectArea(pa_url,
                           myrtcclient,
                           utils_test.pa2)

    @pytest.fixture
    def mock_get_roles(self, mocker):
        # TODO: add roles.xml
        mocked_get = mocker.patch("requests.get")
        mock_resp = mocker.MagicMock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.content = utils_test.read_fixture("roles.xml")
        mocked_get.return_value = mock_resp
        return mocked_get

    def test_get_roles(self, mypa, mock_get_roles, myrtcclient):
        # Role1
        role1_url = "/".join(["http://test.url:9443/jazz/process/project-areas",
                              "_vsoCMN-TEd6VxeRBsGx82Q/roles/Product%20Owner"])
        role1 = Role(role1_url,
                     myrtcclient,
                     utils_test.role1)
        assert str(role1) == "Product Owner"
        assert role1.url == role1_url
        assert role1.id == "Product Owner"
        assert role1.description == " ".join(["The person responsible for",
                                              "managing the Product Backlog."])

        # Role2
        role2_url = "/".join(["http://test.url:9443/jazz/process/project-areas",
                              "_vsoCMN-TEd6VxeRBsGx82Q/roles/Test%20Team"])
        role2 = Role(role2_url,
                     myrtcclient,
                     utils_test.role2)

        # Role3
        role3_url = "/".join(["http://test.url:9443/jazz/process/project-areas",
                              "_vsoCMN-TEd6VxeRBsGx82Q/roles/default"])
        role3 = Role(role3_url,
                     myrtcclient,
                     utils_test.role3)

        roles = mypa.getRoles()
        assert roles == [role1, role2, role3]

    def test_get_role(self, mypa, mock_get_roles, myrtcclient):
        # invalid role labels
        invalid_labels = ["", None, True, False]
        for invalid_label in invalid_labels:
            with pytest.raises(BadValue):
                mypa.getRole(invalid_label)

        # valid role label
        role = mypa.getRole("Product Owner")

        # Role1
        role1_url = "/".join(["http://test.url:9443/jazz/process/project-areas",
                              "_vsoCMN-TEd6VxeRBsGx82Q/roles/Product%20Owner"])
        role1 = Role(role1_url,
                     myrtcclient,
                     utils_test.role1)
        assert role == role1

        # undefined role
        with pytest.raises(NotFound):
            mypa.getRole("fake_role")

    @pytest.fixture
    def mock_get_members(self, mocker):
        mocked_get = mocker.patch("requests.get")
        mock_resp = mocker.MagicMock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.content = utils_test.read_fixture("members.xml")
        mocked_get.return_value = mock_resp
        return mocked_get

    def test_get_members(self, mypa, mock_get_members, myrtcclient):

        # Member1
        m1 = Member("http://test.url:9443/jts/users/tester1%40email.com",
                    myrtcclient,
                    utils_test.member1)
        assert str(m1) == "tester1"
        assert m1.email == "tester1@email.com"
        assert m1.userId == "tester1@email.com"
        assert m1.title =="tester1"
        assert m1.emailAddress == "mailto:tester1%40email.com"
        assert m1.photo is None
        assert m1.modified == "2009-11-24T19:14:14.595Z"
        assert m1.modifiedBy == "ADMIN"

        # Member2
        m2 = Member("http://test.url:9443/jts/users/tester2%40email.com",
                    myrtcclient,
                    utils_test.member2)
        assert str(m2) == "tester2"
        assert m2.email == "tester2@email.com"
        assert m2.userId == "tester2@email.com"
        assert m2.title =="tester2"
        assert m2.emailAddress == "mailto:tester2%40email.com"
        assert m2.photo is None
        assert m2.modified == "2013-04-22T06:24:34.661Z"
        assert m2.modifiedBy == "ADMIN"

        # Member3
        m3 = Member("http://test.url:9443/jts/users/tester3%40email.com",
                    myrtcclient,
                    utils_test.member3)
        assert str(m3) == "tester3"
        assert m3.email == "tester3@email.com"
        assert m3.userId == "tester3@email.com"
        assert m3.title =="tester3"
        assert m3.emailAddress == "mailto:tester3%40email.com"
        assert m3.photo is None
        assert m3.modified == "2010-05-13T20:34:05.138Z"
        assert m3.modifiedBy == "ADMIN"

        members = mypa.getMembers()
        assert members == [m1, m2, m3]

    def test_get_member(self, mypa, myrtcclient, mock_get_members):
        # invalid email address
        invalid_emails = ["", None, True, False, "test.com",
                          "test%40email.com"]
        for invalid_email in invalid_emails:
            with pytest.raises(BadValue):
                mypa.getMember(invalid_email)

        # valid email address
        member = mypa.getMember("tester1@email.com")

        # Member1
        m1 = Member("http://test.url:9443/jts/users/tester1%40email.com",
                    myrtcclient,
                    utils_test.member1)
        assert member == m1

        # undefined member
        with pytest.raises(NotFound):
            mypa.getMember("fake@email.com")

    @pytest.fixture
    def mock_get_itemtypes(self, mocker):
        mocked_get = mocker.patch("requests.get")
        mock_resp = mocker.MagicMock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.content = utils_test.read_fixture("itemtypes.xml")
        mocked_get.return_value = mock_resp
        return mocked_get

    def test_get_itemtypes(self, mypa, mock_get_itemtypes, myrtcclient):
        # ItemType1
        it1_url = "/".join(["http://test.url:9443/jazz/oslc",
                            "types/_CuZu0HUwEeKicpXBddtqNA/defect"])
        it1 = ItemType(it1_url,
                       myrtcclient,
                       utils_test.itemtype1)
        assert it1.url == it1_url
        assert str(it1) == "Defect"
        assert it1.identifier == "defect"
        assert it1.title == "Defect"
        assert it1.iconUrl == "".join(["http://test.url:9443/jazz/service/",
                                       "com.ibm.team.workitem.common.",
                                       "internal.model.IImageContentService/",
                                       "processattachment/",
                                       "_CuZu0HUwEeKicpXBddtqNA/workitemtype",
                                       "/bug.gif"])
        assert it1.dimmedIconUrl is None
        assert it1.category == "defect_task"
        # fake data: pls ignore the value
        assert it1.projectArea == ["Defect", "Task"]

        # ItemType2
        it2_url = "/".join(["http://test.url:9443/jazz/oslc",
                            "types/_CuZu0HUwEeKicpXBddtqNA/task"])
        it2 = ItemType(it2_url,
                       myrtcclient,
                       utils_test.itemtype2)
        assert it2.url == it2_url
        assert str(it2) == "Task"
        assert it2.identifier == "task"
        assert it2.title == "Task"
        assert it2.iconUrl == "".join(["http://test.url:9443/jazz/service/",
                                       "com.ibm.team.workitem.common.",
                                       "internal.model.IImageContentService/",
                                       "processattachment/",
                                       "_CuZu0HUwEeKicpXBddtqNA/workitemtype",
                                       "/task.gif"])
        assert it2.dimmedIconUrl is None
        assert it2.category == "task"
        # fake data: pls ignore the value
        assert it2.projectArea == ["Defect", "Task"]

        its = mypa.getItemTypes()
        assert its == [it1, it2]

    def test_get_itemtype(self, mypa, myrtcclient, mock_get_itemtypes):
        # invalid email address
        invalid_titles = ["", None, True, False]
        for invalid_title in invalid_titles:
            with pytest.raises(BadValue):
                mypa.getItemType(invalid_title)

        # ItemType1
        it1_url = "/".join(["http://test.url:9443/jazz/oslc",
                            "types/_CuZu0HUwEeKicpXBddtqNA/defect"])
        it1 = ItemType(it1_url,
                       myrtcclient,
                       utils_test.itemtype1)

        itemtype = mypa.getItemType("Defect")
        assert itemtype == it1

        # undefined type
        with pytest.raises(NotFound):
            mypa.getItemType("fake_type")

    @pytest.fixture
    def mock_get_admins(self, mocker):
        mocked_get = mocker.patch("requests.get")
        mock_resp = mocker.MagicMock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.content = utils_test.read_fixture("administrators.xml")
        mocked_get.return_value = mock_resp
        return mocked_get

    def test_get_admins(self, mypa, mock_get_admins, myrtcclient):
        # Administrator
        admin_url = "http://test.url:9443/jts/users/tester1%40email.com"
        admin = Administrator(admin_url,
                              myrtcclient,
                              utils_test.admin)
        assert str(admin) == "tester1"
        assert admin.url == admin_url
        assert admin.userId == "tester1@email.com"
        assert admin.title == "tester1"
        assert admin.emailAddress == "mailto:tester1%40email.com"
        assert admin.photo is None
        assert admin.modified == "2009-08-17T10:08:03.721Z"
        assert admin.modifiedBy == "ADMIN"

        admins = mypa.getAdministrators()
        assert admins == [admin]

    def test_get_admin(self, mypa, myrtcclient, mock_get_admins):
        # invalid email address
        invalid_emails = ["", None, True, False, "test.com",
                          "test%40email.com"]
        for invalid_email in invalid_emails:
            with pytest.raises(BadValue):
                mypa.getAdministrator(invalid_email)

        # valid email address
        admin = mypa.getAdministrator("tester1@email.com")

        # Administrator
        ad = Administrator("http://test.url:9443/jts/users/tester1%40email.com",
                           myrtcclient,
                           utils_test.admin)
        assert admin == ad

        # undefined admin
        with pytest.raises(NotFound):
            mypa.getAdministrator("fake@email.com")
