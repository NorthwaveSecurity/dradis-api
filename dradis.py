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

    # Generic action to contact dradis and return the result as JSON
    # Internal use only
    def _action(self, url, header, req_type, **kwargs):

        response = None
        try:
            response = requests.request(req_type, url, headers=header, verify=self.__verify, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise DradisException from e

        if (self.__debug):
            print("\nServer Response:\n")
            print(response.status_code)
            print("---\n")
            print(response.content)

        return response.json()

    # Generic function to get all from an endpoint
    def _get_all(self, endpoint: str) -> list:
        # BUILD URL
        url = self.__url+endpoint

        # HTTP REQUEST TYPE
        req_type = "GET"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type)

        return result

    # Generic function to get all from an endpoint for an id
    def _get_by_id(self, endpoint: str, id: int) -> list:

        # BUILD API ENDPOINT
        url = self.__url + endpoint + "/" + str(id)

        # HTTP REQUEST TYPE
        req_type = "GET"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type)

        return result

    # Generic function to create for an endpoint
    def _create(self, endpoint, data) -> list:

        # BUILD API ENDPOINT
        url = self.__url + endpoint

        # HTTP REQUEST TYPE
        req_type = "POST"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type, json=data)

        return result

    # Generic function to update for an endpoint
    def _update(self, endpoint: str, id: int, data) -> list:

        # BUILD API ENDPOINT
        url = self.__url + endpoint + "/" + str(id)

        # HTTP REQUEST TYPE
        req_type = "PUT"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type, json=data)

        return result

    # Generic function to delete for an endpoint for an id
    def _delete(self, endpoint: str, id: int) -> list:

        # API ENDPOINT
        url = self.__url + endpoint + "/" + str(id)

        # HTTP REQUEST TYPE
        req_type = "DELETE"

        # SET HEADERS
        header = self.__headers

        # GET RESULT
        result = self._action(url=url, header=header, req_type=req_type)

        return result

    # Some API calls require a project id header. These functions get called
    # to facilitate that. Internal use only.
    # Example:
    #   - Add header (id)
    #   - Get result
    #   - remove header
    #   - return result
    # NOTE: EXPECT THE HEADER TO DISAPPEAR IN NEWER DRADIS API VERSIONS!
    def _add_project_header(self, project_id: int) -> None:
        self.__headers["Dradis-Project-Id"] = str(project_id)

    def _cleanup_project_header(self) -> None:
        self.__headers.pop('Dradis-Project-Id', None)

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL TEAMS ENDPOINTS                 #
    #                                                   #
    #####################################################

    # GET ALL TEAM INFO FROM DRADIS
    def get_all_teams(self):

        # Call get all function with teams API name
        return self._get_all(endpoint=self._TEAMS)

    # GET TEAM INFO BY ID
    # REQUIRED:
    #      - team_id -> The id of the team
    def get_team(self, team_id: int) -> list:

        # Call the get by id with endpoint name and id
        return self._get_by_id(endpoint=self._TEAMS, id=team_id)

    # CREATE A NEW TEAM
    # REQUIRED:
    #   - Name -> Name of the new team
    # OPTIONAL:
    #   - team_since -> When the team joined, default is today (YYYY-MM-DD)
    def create_team(self, team_name: str, team_since="") -> list:

        # DATA TO SEND
        team_data = {"team": {"name": "{}".format(team_name), "team_since": "{}".format(team_since)}}

        # Call the create function with endpoint name, data and id.
        return self._create(endpoint=self._TEAMS, data=team_data)

    # UPDATE A TEAM
    # REQUIRED:
    #   - ID -> ID of the team
    # OPTIONAL:
    #   - Name -> Name of the team
    #   - team_since -> When the client joined, default is today (YYYY-MM-DD)
    def update_team(self, team_id: int, team_name=None, team_since=None) -> list:

        # Inital data set
        team_data = {"team": {}}

        # Check what needs to be updated
        if team_name:
            team_data["team"]["name"] = team_name
        if team_since:
            team_data["team"]["team_since"] = team_since

        # Call the update function with endpoint name, data and id.
        return self._update(endpoint=self._TEAMS, data=team_data, id=team_id)

    # DELETE A TEAM
    # REQUIRED:
    #   - team_id -> ID of the team to delete
    def delete_team(self, team_id: int) -> dict:

        # Call the Delete function with endpoint name and id
        return self._delete(endpoint=self._TEAMS, id=team_id)

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL PROJECT ENDPOINTS               #
    #                                                   #
    #####################################################

    # GET ALL PROJECT INFO FROM DRADIS
    def get_all_projects(self):
        # Call get all function with teams API name
        return self._get_all(endpoint=self._PROJECT)

    # GET PROJECT INFO BY ID
    # REQUIRED:
    #      - project_id -> The id of the project
    def get_project(self, project_id: int) -> list:

        # Call the get by id with endpoint name and id
        return self._get_by_id(endpoint=self._PROJECT, id=project_id)

    # CREATE A NEW PROJECT
    # REQUIRED:
    #   - project_name -> name of the project
    #   - client_id -> id of the customer associated with the project
    # OPTIONAL:
    #   - report_template_id -> default report id for valiation
    #   - author_ids -> array with dict containing mailaddress of persons who needs
    #                   access ([{'email': 'redteam@northwave.nl'}])
    #   - template -> NAME of the template for this project
    def create_project(self, project_name: str, client_id: int, report_template_id=0,
                       author_ids=[], template="") -> list:

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

    # UPDATE A PROJECT
    # REQUIRED:
    #   - project_id -> the id of the project to update
    # OPTIONAL:
    #   - project_name -> name of the project
    #   - client_id -> id of the customer associated with the project
    #   - report_template_id -> default report id for valiation
    #   - author_ids -> array with dict containing mailaddress of persons who needs
    #                   access ([{'email': 'redteam@northwave.nl'}])
    #   - template -> NAME of the template for this project
    def update_project(self, project_id: int, project_name=None, client_id=None, report_template_id=None,
                       author_ids=None, template=None) -> list:

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

    # DELETE A PROJECT
    # REQUIRED:
    #   - project_id -> ID of the project to delete
    def delete_project(self, project_id: int) -> list:

        # Call the delete endpoint with the project id
        return self._delete(endpoint=self._PROJECT, id=project_id)

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL NODES ENDPOINTS                 #
    #                                                   #
    #####################################################

    # GET ALL EVIDENCE NODES FOR A SPECIFIC PROJECT
    # REQUIRED:
    #   - project_id -> ID for the project for the nodes
    def get_all_nodes(self, project_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_all(endpoint=self._NODE)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # GET A SPECIFIC NODE FOR A SPECIFIC PROJECT
    # REQUIRED:
    #   - project_id -> ID for the project for the node
    #   - node_id -> ID for the node to get
    def get_node(self, project_id: int, node_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_by_id(endpoint=self._NODE, id=node_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_or_create_node(self, project_id: int, label: str):
        node = self.get_node_by_label(project_id, label)
        if not node:
            return self.create_node(project_id=project_id, label=label, type_id=1)
        return node

    # CREATE NEW NODE
    # REQUIRED:
    #   - project_id -> the id of the project to insert the node at
    #   - label -> the label for the new node
    #   - type_id -> the type of node.
    #            0 to create a notes node (like Intro, summary)
    #            1 to create endpoint node (website, ip, app)
    #   - parent_id -> Id of the parent node
    # OPTIONAL:
    #   - position -> the position of the insertion, default at the top (0)
    def create_node(self, project_id: int, label: str, type_id: int, parent_id=None, position=0) -> list:

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

    # UPDATE A NODE
    # REQUIRED:
    #   - project_id -> the id of the project
    #   - node_id -> the node to update
    # OPTIONAL:
    #   - label -> the label for the  node
    #   - type_id -> the type of node.
    #            0 to create a notes node (like Intro, summary)
    #            1 to create endpoint node (website, ip, app)
    #   - parent_id -> Id of the parent node
    #   - position -> the position of the insertion
    def update_node(self, project_id: int, node_id: int, label=None, type_id=None,
                    parent_id=None, position=None) -> list:

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

    # DELETE A NODE
    # Required:
    #   - project_id -> the id of the project the node exists at
    #   - node_id -> Id of the node to delete
    def delete_node(self, project_id: int, node_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._NODE, id=node_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL ISSUES ENDPOINTS                #
    #                                                   #
    #####################################################

    # GET ALL ISSUES FOR A SPECIFIC PROJECT
    # REQUIRED:
    #   - project_id -> ID for the project for the issue
    def get_all_issues(self, project_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_all(endpoint=self._ISSUE)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # GET ALL EVIDENCE NODES FOR A SPECIFIC PROJECT
    # REQUIRED:
    #   - project_id -> ID for the project for the nodes
    #   - issue_id -> ID for the issue to get
    def get_issue(self, project_id: int, issue_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Fetch result from dradis
        result = self._get_by_id(endpoint=self._ISSUE, id=issue_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # CREATE NEW ISSUE
    # REQUIRED:
    #   - project_id -> the id of the project to insert the node at
    #   - text -> Content of the issue
    def create_issue(self, project_id: int, text: str) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Set the node data
        node_data = {"issue": {"text": text}}

        # Grab the result
        result = self._create(endpoint=self._ISSUE, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # UPDATE ISSUE
    # REQUIRED:
    #   - project_id -> the id of the project to insert the node at
    #   - text -> Content of the issue
    def update_issue(self, project_id: int, issue_id: int, text: str) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Set the node data
        node_data = {"issue": {"text": text}}

        # Grab the result
        result = self._update(endpoint=self._ISSUE, id=issue_id, data=node_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # DELETE AN ISSUE
    # Required:
    #   - project_id -> the id of the project the node exists at
    #   - node_id -> Id of the node to delete
    def delete_issue(self, project_id: int, issue_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._ISSUE, id=issue_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL EVIDENCE ENDPOINTS              #
    #                                                   #
    #####################################################

    # GET ALL EVIDENCE FOR A SPECIFIC NODE IN A SPECIFIC PROJECT
    # REQUIRED:
    #   - project_id -> ID for the project for the evidence
    #   - node_id -> ID for the node for the project for the evidence
    def get_all_evidence(self, project_id: int, node_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Fetch result from dradis
        result = self._get_all(endpoint=endpoint)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # GET SPECIFIC EVIDENCE FOR A SPECIFIC PROJECT
    # REQUIRED:
    #   - project_id -> ID for the project for the issue
    #   - node_id -> ID for the node for the project for the evidence
    #   - evidence_id -> ID for the evidence for the project
    def get_evidence(self, project_id: int, node_id: int, evidence_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Fetch result from dradis
        result = self._get_by_id(endpoint=endpoint, id=evidence_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # CREATE NEW EVIDENCE
    # REQUIRED:
    #   - project_id -> the id of the project to insert the evidence at
    #   - node_id -> ID for the node for the project for the evidence
    #   - issue_id -> ID of the isssue to attach the evidence too
    #   - content -> Actual evidence content
    def create_evidence(self, project_id: int, node_id: int, issue_id: int, content: str) -> list:

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

    # UPDATE EVIDENCE
    # REQUIRED:
    #   - project_id -> the id of the project to update the evidence at
    #   - node_id -> ID for the node for the project for the evidence
    #   - issue_id -> ID of the isssue to attach the evidence too
    #   - content -> Actual evidence content
    def update_evidence(self, project_id: int, node_id: int, issue_id: int, evidence_id: int, content: str) -> list:

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

    # DELETE AN ISSUE
    # Required:
    #   - project_id -> the id of the project the node exists at
    #   - node_id -> Id of the node to delete the evidence at
    #   - evidence_id -> ID of the evidence to delete
    def delete_evidence(self, project_id: int, node_id: int, evidence_id: int) -> list:

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._EVIDENCE.replace("<node_id>", str(node_id))

        # Get the result
        result = self._delete(endpoint=endpoint, id=evidence_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #            ALL CONTENT BLOCKS ENDPOINTS           #
    #                                                   #
    #####################################################

    # GET ALL CONTENTBLOCKS FROM PROJECT
    # REQUIRED:
    #   - project_id -> id of the project to get the content block from
    def get_all_contentblocks(self, project_id: int):
        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_all(endpoint=self._CONTENTBLOCK)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # GET SPECIFIC CONTENTBLOCK
    # REQUIRED:
    #   - project_id -> id of the project to get the content block from
    #   - contentblock_id -> id of the contentblock for the project
    def get_contentblock(self, project_id: int, contentblock_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_by_id(endpoint=self._CONTENTBLOCK, id=contentblock_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # CREATE NEW CONTENTBLOCK
    # REQUIRED:
    #   - project_id -> id of the project to get the content block from
    #   - content -> content of the content block
    # OPTIONAL:
    #   - blockgroupname -> Name of the group this content is associated with (Conclusions ,intro, etc.)
    def create_contentblock(self, project_id: int, content: str, blockgroupname=None):

        # Add required header to set
        self._add_project_header(project_id)

        # Create the data set
        content_data = {"content_block": {"content": content, "block_group": blockgroupname}}

        # Get the result
        result = self._create(endpoint=self._CONTENTBLOCK, data=content_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # UPDATE CONTENTBLOCK
    # REQUIRED:
    #   - project_id -> id of the project to get the content block from
    #   - contentblock_id -> id of the content block to update
    # OPTIONAL:
    #   - blockgroupname -> Name of the group this content is associated with (Conclusions ,intro, etc.)
    #   - content -> content of the content block
    def update_contentblock(self, project_id: int, contentblock_id: int, content=None, blockgroupname=None):
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

    # DELETE SPECIFIC CONTENTBLOCK
    # REQUIRED:
    #   - project_id -> id of the project to delete the content block from
    #   - contentblock_id -> id of the contentblock for the project
    def delete_contentblock(self, project_id: int, contentblock_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._CONTENTBLOCK, id=contentblock_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #               ALL NOTES ENDPOINTS                 #
    #                                                   #
    #####################################################

    # GET ALL NOTES FROM PROJECT
    # REQUIRED:
    #   - project_id -> id of the project to get the note from
    #   - node_id -> the id of the noDe to get all the noTes from
    def get_all_notes(self, project_id: int, node_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_all(endpoint=endpoint)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # GET SPECIFIC NOTE FROM PROJECT
    # REQUIRED:
    #   - project_id -> id of the project to get the note from
    #   - node_id -> the id of the noDe to get the noTe from
    #   - note_id -> the id of the noTe to get
    def get_note(self, project_id: int, node_id: int, note_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_by_id(endpoint=endpoint, id=note_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    # CREATE A NEW NODE
    # REQUIRED:
    #   - project_id -> id of the project to create the note at
    #   - node_id -> the id of the noDe to create the noTe at
    #   - text -> Content of the note
    # OPTIONAL:
    #   - category_id -> the id of the category (i.e. 1 for 'AdvancedWordExport Ready')
    def create_note(self, project_id: int, node_id: int, text: str, category_id=None):

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

    # UPDATE A NOTE
    # REQUIRED:
    #   - project_id -> id of the project to update the note at
    #   - node_id -> the id of the noDe to update the noTe at
    #   - note_id -> the id of the noTe to update
    #   - text -> Content of the note
    # OPTIONAL:
    #   - category_id -> the id of the category (i.e. 1 for 'AdvancedWordExport Ready')
    def update_note(self, project_id: int, node_id: int, note_id: int, text: str, category_id=None):

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

    # DELETE SPECIFIC NOTE FROM PROJECT
    # REQUIRED:
    #   - project_id -> id of the project to delete the note from
    #   - node_id -> the id of the noDe to delete the noTe from
    #   - note_id -> the id of the noTe to delete
    def delete_note(self, project_id: int, node_id: int, note_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._delete(endpoint=endpoint, id=note_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #           ALL ATTACHMENTS ENDPOINTS               #
    #                                                   #
    #####################################################
    #            !!!NOT IN USE AS THEY SUCK!!!          #
    def get_all_attachments(self, project_id: int, node_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_all(endpoint=endpoint)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_attachment(self, project_id: int, node_id: int, attachment_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._ATTACHMENT.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._get_by_id(endpoint=endpoint, id=attachment_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_attachment(self, project_id: int, node_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        # endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Set the data
        # data = {}

        # Grab the result
        result = []

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_attachment(self, project_id: int, node_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        # endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Set the data
        # data = {}

        # Grab the result
        result = []

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def delete_attachment(self, project_id: int, node_id: int, attachment_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        endpoint = self._NOTE.replace("<node_id>", str(node_id))

        # Grab the result
        result = self._delete(endpoint=endpoint, id=attachment_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #         ALL DOCUMENT PROPERTIES ENDPOINTS         #
    #                                                   #
    #####################################################

    def get_all_docprops(self, project_id: int):
        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_all(endpoint=self._DOCPROPS)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def get_docprop(self, project_id: int, docprops_id: int):

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._get_by_id(endpoint=self._DOCPROPS, id=docprops_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def create_docprop(self, project_id: int, properties: dict):

        # Add required header to set
        self._add_project_header(project_id)

        doc_data = {"document_properties": properties}

        # Get the result
        result = self._create(endpoint=self._DOCPROPS, data=doc_data)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    def update_docprop(self, project_id: int, docprops_id: str, text: str):

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

        # Add required header to set
        self._add_project_header(project_id)

        # Get the result
        result = self._delete(endpoint=self._DOCPROPS, id=docprops_id)

        # Cleanup headers
        self._cleanup_project_header()

        return result

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #         ALL ISSUELIBRARY ENDPOINTS                #
    #                                                   #
    #####################################################

    def get_all_standard_issues(self):
        return self._get_all(endpoint=self._ISSUE_LIB)

    def get_standard_issue(self, issue_id: int):
        return self._get_by_id(endpoint=self._ISSUE_LIB, id=issue_id)

    def create_standard_issue(self, issue_content: str):
        issue_data = {"entry": {"content": issue_content}}
        return self._create(endpoint=self._ISSUE_LIB, data=issue_data)

    def update_standard_issue(self, issue_id: int, issue_content: str):
        issue_data = {"entry": {"content": issue_content}}
        return self._update(endpoint=self._ISSUE_LIB, id=issue_id, data=issue_data)

    def delete_standard_issue(self, issue_id: int):
        return self._delete(endpoint=self._ISSUE_LIB, id=issue_id)

    #####################################################
    # ------------------------------------------------- #
    #####################################################

    #####################################################
    #                                                   #
    #                   UTILITY METHODS                 #
    #                                                   #
    #####################################################

    def node_exists(self, label: str, project_id: int):
        return self.__exists(value_name='label',
                             value_to_check=label,
                             list_to_check=self.get_all_nodes(project_id=project_id))

    def issue_exists(self, title: str, project_id: int):
        return self.__exists(value_name='title',
                             value_to_check=title,
                             list_to_check=self.get_all_issues(project_id=project_id))

    def get_issue_by_title(self, title: str, project_id: int):
        for issue in self.get_all_issues(project_id=project_id):
            if issue.get('title', None) == title:
                return issue

    def get_node_by_label(self, project_id: int, label: str):
        for n in self.get_all_nodes(project_id):
            if n['label'] == label:
                return n
        return None

    def __exists(self, value_name: str, value_to_check: str, list_to_check: list):
        return any(d.get(value_name, None) == value_to_check for d in list_to_check)
