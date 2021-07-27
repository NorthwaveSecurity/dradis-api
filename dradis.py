#####################################################################################
#                  dradis-python: Python Wrapper for Dradis API v1.0                #
#                       Copyright (c) 2019 Northwave B.V.                           #
#                           Author: Frank de Korte                                  #
#####################################################################################
import requests


class DradisException(Exception):
    pass


class Dradis():

    # API ENDPOINTS
    _TEAMS = "/pro/api/teams"
    _PROJECT = "/pro/api/projects"
    _NODE = "/pro/api/nodes"
    _ISSUE = "/pro/api/issues"
    _EVIDENCE = "/pro/api/nodes/<node_id>/evidence"
    _CONTENTBLOCK = "/pro/api/content_blocks"
    _NOTE = "/pro/api/nodes/<node_id>/notes"
    _ATTACHMENT = "/pro/api/nodes/<node_id>/attachments"
    _DOCPROPS = "/pro/api/document_properties"
    _ISSUE_LIB = "/pro/api/addons/issuelib/entries"

    def __init__(self, api_token, url, debug=False, verify=True):
        self.__api_token = api_token  # API Token
        self.__url = url              # Dradis URL (eg. https://your_dradis_server.com)
        self.__debug = debug          # Debuging True?
        self.__verify = verify        # Verify SSL
        self.__headers = {
            'Authorization': 'Token token={}'.format(self.__api_token),
            'Content-type': 'application/json',
            'Accept': 'application/vnd.dradisproapi; v=1'
        }  # Default headers

    #####################################################
    #                                                   #
    #   GENERIC ACTION FUNCTION WRAPPERS TO DRADIS API  #
    #                                                   #
    #####################################################

    def _action(self, url, header, req_type, **kwargs):
        """Generic action to contact dradis and return the result as JSON
        Internal use only"""

        response = None
        try:
            response = requests.request(req_type, url, headers=header, verify=self.__verify, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise DradisException from e

        if (self.__debug):
            print("\nRequest url:\n")
            print(url)
            print("\nServer Response:\n")
            print(response.status_code)
            print("---\n")
            print(response.content)

        return response.json()

    def _get_all(self, endpoint: str) -> list:
        """Generic function to get all from an endpoint"""

        # BUILD URL
        url = self.__url+endpoint

        # HTTP REQUEST TYPE
        req_type = "GET"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type)

        return result

    def _get_by_id(self, endpoint: str, id: int) -> list:
        """Generic function to get all from an endpoint for an id"""

        # BUILD API ENDPOINT
        url = self.__url + endpoint + "/" + str(id)

        # HTTP REQUEST TYPE
        req_type = "GET"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type)

        return result

    def _create(self, endpoint, data) -> list:
        """Generic function to create for an endpoint"""

        # BUILD API ENDPOINT
        url = self.__url + endpoint

        # HTTP REQUEST TYPE
        req_type = "POST"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type, json=data)

        return result

    def _update(self, endpoint: str, id: int, data) -> list:
        """Generic function to update for an endpoint"""

        # BUILD API ENDPOINT
        url = self.__url + endpoint + "/" + str(id)

        # HTTP REQUEST TYPE
        req_type = "PUT"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type, json=data)

        return result

    def _delete(self, endpoint: str, id: int) -> list:
        """Generic function to delete for an endpoint for an id"""

        # API ENDPOINT
        url = self.__url + endpoint + "/" + str(id)

        # HTTP REQUEST TYPE
        req_type = "DELETE"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type)

        return result

    def _add_project_header(self, project_id: int) -> None:
        """Some API calls require a project id header. These functions get called
        to facilitate that. Internal use only.
        Example:
          - Add header (id)
          - Get result
          - remove header
          - return result
        NOTE: EXPECT THE HEADER TO DISAPPEAR IN NEWER DRADIS API VERSIONS!"""
        self.__headers["Dradis-Project-Id"] = str(project_id)

    def _cleanup_project_header(self) -> None:
        """Remove the project id header"""
        self.__headers.pop('Dradis-Project-Id', None)

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL TEAMS ENDPOINTS                 #
    #                                                   #
    #####################################################

    def get_all_teams(self):
        """Get all team info from dradis"""

        # Call get all function with teams API name
        return self._get_all(endpoint=self._TEAMS)

    def get_team(self, team_id: int) -> list:
        """Get team info by id

        :param team_id: The id of the team
        """

        # Call the get by id with endpoint name and id
        return self._get_by_id(endpoint=self._TEAMS, id=team_id)

    def create_team(self, team_name: str, team_since="") -> list:
        """Create a new team

        :param Name: Name of the new team
        :param team_since: When the team joined, default is today (YYYY-MM-DD)
        """

        # data to send
        team_data = {"team": {"name": "{}".format(team_name), "team_since": "{}".format(team_since)}}

        # Call the create function with endpoint name, data and id.
        return self._create(endpoint=self._TEAMS, data=team_data)

    def update_team(self, team_id: int, team_name=None, team_since=None) -> list:
        """Update a team

        :param ID: ID of the team
        :param Name: Name of the team
        :param team_since: When the client joined, default is today (YYYY-MM-DD)
        """

        # Inital data set
        team_data = {"team": {}}

        # Check what needs to be updated
        if team_name:
            team_data["team"]["name"] = team_name
        if team_since:
            team_data["team"]["team_since"] = team_since

        # Call the update function with endpoint name, data and id.
        return self._update(endpoint=self._TEAMS, data=team_data, id=team_id)

    def delete_team(self, team_id: int) -> dict:
        """Delete a team

        :param team_id: ID of the team to delete
        """

        # Call the Delete function with endpoint name and id
        return self._delete(endpoint=self._TEAMS, id=team_id)

    #####################################################
    #                                                   #
    #               ALL PROJECT ENDPOINTS               #
    #                                                   #
    #####################################################

    def get_all_projects(self):
        """Get all project info from dradis"""

        # Call get all function with teams API name
        return self._get_all(endpoint=self._PROJECT)

    def get_project(self, project_id: int) -> list:
        """Get project info by id

        :param project_id: The id of the project
        """

        # Call the get by id with endpoint name and id
        return self._get_by_id(endpoint=self._PROJECT, id=project_id)

    def create_project(self, project_name: str, client_id: int, report_template_id=0,
                       author_ids=[], template="") -> list:
        """Create a new project

        :param project_name: Name of the project
        :param client_id: Id of the customer associated with the project
        :param report_template_id: Default report id for valiation
        :param author_ids: Array with dict containing mailaddress of persons who needs
                          access ([{'email': 'alice@example.com'}])
        :param template: Name of the template for this project
        """

        # Create project data
        project_data = {
            "project": {
                "name": "{}".format(project_name),
                "client_id": "{}".format(client_id),
                "report_template_properties_id": "{}".format(report_template_id),
                "author_ids": author_ids,
                "template": "{}".format(template)}
        }

        return self._create(endpoint=self._PROJECT, data=project_data)

    def update_project(self, project_id: int, project_name=None, client_id=None, report_template_id=None,
                       author_ids=None, template=None) -> list:
        """Update a project

        :param project_id: The id of the project to update
        :param project_name: Name of the project
        :param client_id: Id of the customer associated with the project
        :param report_template_id: Default report id for valiation
        :param author_ids: Array with dict containing mailaddress of persons who needs
                          access ([{'email': 'test@example.com'}])
        :param template: Name of the template for this project
        """

        # Create project data
        project_data = {"project": {}}

        # Check what needs to be changed
        if project_name:
            project_data["project"]["project_name"] = project_name
        if client_id:
            project_data["project"]["client_id"] = client_id
        if report_template_id:
            project_data["project"]["report_template_id"] = report_template_id
        if author_ids:
            project_data["project"]["author_ids"] = author_ids
        if template:
            project_data["project"]["template"] = template

        return self._update(endpoint=self._PROJECT, id=project_id, data=project_data)

    def delete_project(self, project_id: int) -> list:
        """Delete a project

        :param project_id: ID of the project to delete
        """

        # Call the delete endpoint with the project id
        return self._delete(endpoint=self._PROJECT, id=project_id)

    #####################################################
    #                                                   #
    #               ALL NODES ENDPOINTS                 #
    #                                                   #
    #####################################################

    def get_all_nodes(self, project_id: int) -> list:
        """Get all evidence nodes for a specific project

        :param project_id: ID for the project for the nodes
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_all(endpoint=self._NODE)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_node(self, project_id: int, node_id: int) -> list:
        """Get a specific node for a specific project

        :param project_id: ID for the project for the node
        :param node_id: ID for the node to get
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_by_id(endpoint=self._NODE, id=node_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_or_create_node(self, project_id: int, label: str):
        """Get a node by label or create it if it does not exist

        :returns: The node
        """

        node = self.get_node_by_label(project_id, label)
        if not node:
            return self.create_node(project_id=project_id, label=label, type_id=1)
        return node

    def create_node(self, project_id: int, label: str, type_id: int, parent_id=None, position=0) -> list:
        """Create new node

        :param project_id: The id of the project to insert the node at
        :param label: The label for the new node
        :param type_id: The type of node.
                   0 to create a notes node (like Intro, summary)
                   1 to create endpoint node (website, ip, app)
        :param parent_id: Id of the parent node
        :param position: The position of the insertion, default at the top (0)
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Set the node data
        node_data = {
            "node": {
                "label": label,
                "type_id": type_id,
                "parent_id": parent_id,
                "position": position
            }
        }

        # Grab the result
        result = self._create(endpoint=self._NODE, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_node(self, project_id: int, node_id: int, label=None, type_id=None,
                    parent_id=None, position=None) -> list:
        """Update a node

        :param project_id: The id of the project
        :param node_id: The node to update
        :param label: The label for the  node
        :param type_id: The type of node.
                   0 to create a notes node (like Intro, summary)
                   1 to create endpoint node (website, ip, app)
        :param parent_id: Id of the parent node
        :param position: The position of the insertion
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Set the node data
        node_data = {"node": {}}

        # IF DATA IS THERE, LETS SEND IT!
        if label:
            node_data["node"]["label"] = label
        if type_id:
            node_data["node"]["type_id"] = type_id
        if parent_id:
            node_data["node"]["parent_id"] = parent_id
        if position:
            node_data["node"]["position"] = position

        # Grab the result
        result = self._update(endpoint=self._NODE, id=node_id, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_node(self, project_id: int, node_id: int) -> list:
        """Delete a node

        :param project_id: The id of the project the node exists at
        :param node_id: Id of the node to delete
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._NODE, id=node_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #               ALL ISSUES ENDPOINTS                #
    #                                                   #
    #####################################################

    def get_all_issues(self, project_id: int) -> list:
        """Get all issues for a specific project

        :param project_id: ID for the project for the issue
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_all(endpoint=self._ISSUE)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_issue(self, project_id: int, issue_id: int) -> list:
        """Get all evidence nodes for a specific project

        :param project_id: ID for the project for the nodes
        :param issue_id: ID for the issue to get
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_by_id(endpoint=self._ISSUE, id=issue_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_issue(self, project_id: int, text: str) -> list:
        """Create new issue

        :param project_id: The id of the project to insert the node at
        :param text: Content of the issue
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Set the node data
        node_data = {"issue": {"text": text}}

        # Grab the result
        result = self._create(endpoint=self._ISSUE, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_issue(self, project_id: int, issue_id: int, text: str) -> list:
        """Update issue

        :param project_id: The id of the project to insert the node at
        :param text: Content of the issue
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Set the node data
        node_data = {"issue": {"text": text}}

        # Grab the result
        result = self._update(endpoint=self._ISSUE, id=issue_id, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_issue(self, project_id: int, issue_id: int) -> list:
        """Delete an issue

        :param project_id: The id of the project the node exists at
        :param node_id: Id of the node to delete
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._ISSUE, id=issue_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #               ALL EVIDENCE ENDPOINTS              #
    #                                                   #
    #####################################################

    def get_all_evidence(self, project_id: int, node_id: int) -> list:
        """Get all evidence for a specific node in a specific project

        :param project_id: ID for the project for the evidence
        :param node_id: ID for the node for the project for the evidence
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Fetch result from dradis
        result = self._get_all(endpoint=endpoint)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_evidence(self, project_id: int, node_id: int, evidence_id: int) -> list:
        """Get specific evidence for a specific project

        :param project_id: ID for the project for the issue
        :param node_id: ID for the node for the project for the evidence
        :param evidence_id: ID for the evidence for the project
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Fetch result from dradis
        result = self._get_by_id(endpoint=endpoint, id=evidence_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_evidence(self, project_id: int, node_id: int, issue_id: int, content: str) -> list:
        """Create new evidence

        :param project_id: the id of the project to insert the evidence at
        :param node_id: ID for the node for the project for the evidence
        :param issue_id: ID of the isssue to attach the evidence too
        :param content: Actual evidence content
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Set the node data
        node_data = {"evidence": {"content": content, "issue_id": str(issue_id)}}

        # Grab the result
        result = self._create(endpoint=endpoint, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_evidence(self, project_id: int, node_id: int, issue_id: int, evidence_id: int, content: str) -> list:
        """Update evidence

        :param project_id: The id of the project to update the evidence at
        :param node_id: ID for the node for the project for the evidence
        :param issue_id: ID of the isssue to attach the evidence too
        :param content: Actual evidence content
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Set the node data
        node_data = {"evidence": {"content": content, "issue_id": str(issue_id)}}

        # Grab the result
        result = self._update(endpoint=endpoint, id=evidence_id, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_evidence(self, project_id: int, node_id: int, evidence_id: int) -> list:
        """Delete an issue

        :param project_id: The id of the project the node exists at
        :param node_id: ID of the node to delete the evidence at
        :param evidence_id: ID of the evidence to delete
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Get the result
        result = self._delete(endpoint=endpoint, id=evidence_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #            ALL CONTENT BLOCKS ENDPOINTS           #
    #                                                   #
    #####################################################

    def get_all_contentblocks(self, project_id: int):
        """Get all contentblocks from project
        :param project_id: Id of the project to get the content block from
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_all(endpoint=self._CONTENTBLOCK)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_contentblock(self, project_id: int, contentblock_id: int):
        """Get specific contentblock

        :param project_id: ID of the project to get the content block from
        :param contentblock_id: ID of the contentblock for the project
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_by_id(endpoint=self._CONTENTBLOCK, id=contentblock_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_contentblock(self, project_id: int, content: str, blockgroupname=None):
        """Create new contentblock

        :param project_id: ID of the project to get the content block from
        :param content: Content of the content block
        :param blockgroupname: Name of the group this content is associated with (Conclusions ,intro, etc.)
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Create the data set
        content_data = {"content_block": {"content": content, "block_group": blockgroupname}}

        # Get the result
        result = self._create(endpoint=self._CONTENTBLOCK, data=content_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_contentblock(self, project_id: int, contentblock_id: int, content=None, blockgroupname=None):
        """Update contentblock

        :param project_id: Id of the project to get the content block from
        :param contentblock_id: Id of the content block to update
        :param blockgroupname: Name of the group this content is associated with (Conclusions ,intro, etc.)
        :param content: Content of the content block
        """

        # Add required header to set
        self._add_project_header(project_id)

        content_data = {"content_block": {}}

        if content:
            content_data["content_block"]["content"] = content
        if blockgroupname:
            content_data["content_block"]["block_group"] = blockgroupname

        # Get the result
        result = self._update(endpoint=self._CONTENTBLOCK, id=contentblock_id, data=content_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_contentblock(self, project_id: int, contentblock_id: int):
        """Delete specific contentblock

        :param project_id: ID of the project to delete the content block from
        :param contentblock_id: ID of the contentblock for the project
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._CONTENTBLOCK, id=contentblock_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #               ALL NOTES ENDPOINTS                 #
    #                                                   #
    #####################################################

    def get_all_notes(self, project_id: int, node_id: int):
        """Get all notes from project

        :param project_id: ID of the project to get the note from
        :param node_id: The id of the noDe to get all the noTes from
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_all(endpoint=endpoint)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_note(self, project_id: int, node_id: int, note_id: int):
        """Get specific note from project

        :param project_id: ID of the project to get the note from
        :param node_id: The id of the noDe to get the noTe from
        :param note_id: The id of the noTe to get
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_by_id(endpoint=endpoint, id=note_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_note(self, project_id: int, node_id: int, text: str, category_id=None):
        """Create a new node

        :param project_id: ID of the project to create the note at
        :param node_id: The id of the noDe to create the noTe at
        :param text: Content of the note
        :param category_id: The id of the category (i.e. 1 for 'AdvancedWordExport Ready')
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Set the data
        note_data = {"note": {"text": text, "category_id": category_id}}

        # Grab the result
        result = self._create(endpoint=endpoint, data=note_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_note(self, project_id: int, node_id: int, note_id: int, text: str, category_id=None):
        """Update a note

        :param project_id: ID of the project to update the note at
        :param node_id: The id of the noDe to update the noTe at
        :param note_id: The id of the noTe to update
        :param text: Content of the note
        :param category_id: The id of the category (i.e. 1 for 'AdvancedWordExport Ready')
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Set the data
        note_data = {"note": {"text": text, "category_id": category_id}}

        # Grab the result
        result = self._update(endpoint=endpoint, id=note_id, data=note_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_note(self, project_id: int, node_id: int, note_id: int):
        """Delete specific note from project

        :param project_id: ID of the project to delete the note from
        :param node_id: The id of the noDe to delete the noTe from
        :param note_id: The id of the noTe to delete
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._delete(endpoint=endpoint, id=note_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #           ALL ATTACHMENTS ENDPOINTS               #
    #                                                   #
    #####################################################
    #            !!!NOT IN USE AS THEY SUCK!!!          #
    #####################################################

    def get_all_attachments(self, project_id: int, node_id: int):
        """Get all attachments

        :param project_id: ID for the project
        :param node_id: ID for the node to get attachments from
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_all(endpoint=endpoint)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_attachment(self, project_id: int, node_id: int, filename: int):
        """Get a single attachment

        :param project_id: ID for the project
        :param node_id: ID for the node to get attachment from
        :param filename: Filename of the attachment
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_by_id(endpoint=endpoint, id=filename)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_attachment(self, project_id: int, node_id: int):
        """Create a new attachment

        :param project_id: ID for the project
        :param node_id: ID for the node to create attachment for
        """

        raise NotImplementedError()

        # Add required header to set
        self._add_project_header(project_id)

        # endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Set the data
        # data = {}

        # Grab the result
        result = []

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def rename_attachment(self, project_id: int, node_id: int, filename: str, new_filename: str):
        """Renames a specific Attachment on a Node in your project

        :param project_id: ID for the project
        :param node_id: ID for the node to update attachment for
        :param filename: The filename of the attachment to update
        :param new_filename: The new filename of the attachment
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Set the data
        data = {"attachment": {"filename": new_filename}}

        # Grab the result
        result = self._update(endpoint, filename, data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_attachment(self, project_id: int, node_id: int, filename: int):
        """Delete an attachment

        :param project_id: ID for the project
        :param node_id: ID for the node to delete attachment from
        :param filename: The filename of the attachment to delete
        """

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._delete(endpoint=endpoint, id=filename)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #         ALL DOCUMENT PROPERTIES ENDPOINTS         #
    #                                                   #
    #####################################################

    def get_all_docprops(self, project_id: int):
        """Get all document properties for a specific project"""

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_all(endpoint=self._DOCPROPS)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_docprop(self, project_id: int, docprops_id: int):
        """Get a specific document property from a project

        :param project_id: ID of the project to get the document property from
        :param docprops_id: ID of the document property
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_by_id(endpoint=self._DOCPROPS, id=docprops_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_docprop(self, project_id: int, properties: dict):
        """Create new document properties for a project

        :param project_id: ID of the project to create the document properties for
        :param properties: Document properties as a dictionary
        """

        # Add required header to set
        self._add_project_header(project_id)

        doc_data = {"document_properties": properties}

        # Get the result
        result = self._create(endpoint=self._DOCPROPS, data=doc_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_docprop(self, project_id: int, docprops_id: str, text: str):
        """Update a specific document property

        :param project_id: ID of the project to update the document property for
        :param docprops_id: ID of the document property to update
        :param text: New text of the document property
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Create list
        doc_data = {"document_property": {"value": text}}

        # Get the result
        result = self._update(endpoint=self._DOCPROPS, id=docprops_id, data=doc_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_docprop(self, project_id: int, docprops_id: str):
        """Delete a document property

        :param project_id: ID of the project to delete the property from
        :param docprops_id: ID of the document property to delete
        """

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._DOCPROPS, id=docprops_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    #                                                   #
    #         ALL ISSUELIBRARY ENDPOINTS                #
    #                                                   #
    #####################################################

    def get_all_standard_issues(self):
        """Get all issues in the issue library"""

        return self._get_all(endpoint=self._ISSUE_LIB)

    def get_standard_issue(self, issue_id: int):
        """Get a specific issue from the issue library"""

        return self._get_by_id(endpoint=self._ISSUE_LIB, id=issue_id)

    def create_standard_issue(self, issue_content: str):
        """Create a new issue in the issue library

        :param issue_content: The content of the issue
        """

        issue_data = {"entry": {"content": issue_content}}
        return self._create(endpoint=self._ISSUE_LIB, data=issue_data)

    def update_standard_issue(self, issue_id: int, issue_content: str):
        """Update an issue in the issue library

        :param issue_id: ID of the standard issue to update
        :param issue_content: The new content of the standard issue
        """

        issue_data = {"entry": {"content": issue_content}}
        return self._update(endpoint=self._ISSUE_LIB, id=issue_id, data=issue_data)

    def delete_standard_issue(self, issue_id: int):
        """Delete an issue from the issue library

        :param issue_id: ID of the issue to delete"""

        return self._delete(endpoint=self._ISSUE_LIB, id=issue_id)

    #####################################################
    #                                                   #
    #                   UTILITY METHODS                 #
    #                                                   #
    #####################################################

    def node_exists(self, label: str, project_id: int):
        """Check if a node with a given label exists for the given project

        :param label: Label to check existence for
        :param project_id: ID of the project to check in
        """

        return self.__exists(value_name='label',
                             value_to_check=label,
                             list_to_check=self.get_all_nodes(project_id=project_id))

    def issue_exists(self, title: str, project_id: int):
        """Check if an issue with a given title exists for the given project

        :param title: Title to check existence for
        :param project_id: ID of the project to check in
        """
        return self.__exists(value_name='title',
                             value_to_check=title,
                             list_to_check=self.get_all_issues(project_id=project_id))

    def get_issue_by_title(self, title: str, project_id: int):
        """Get an issue with the given title

        :param title: Title that the issue should have
        :param project_id: ID of the project to check in

        :returns: The first issue found with the given title or None
        """

        for issue in self.get_all_issues(project_id=project_id):
            if issue.get('title', None) == title:
                return issue
        return None

    def get_node_by_label(self, project_id: int, label: str):
        """Get a node with the given label

        :param label: Label that the node should have
        :param project_id: ID of the project to check in

        :returns: The first node found with the given label or None
        """
        for n in self.get_all_nodes(project_id):
            if n['label'] == label:
                return n
        return None

    def __exists(self, value_name: str, value_to_check: str, list_to_check: list):
        """Check if a specific key-value pair exists in the givel list of dictionaries

        :param value_name: Key to check for
        :param value_to_check: The value that should belong to the key
        :param list_to_check: List of dictionaries that possibly contain the `value_name` key

        :returns: True if the given key-value pair exists in the list, False otherwise"""
        return any(d.get(value_name, None) == value_to_check for d in list_to_check)
