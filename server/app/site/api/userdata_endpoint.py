from flasgger.utils import swag_from  # Specify swagger doc path
from app.site.models.user_data import UserDataModel
from app.site.api.ApiBase import ApiBase, ApiBaseDefault
from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected

SWAGGERDOC_PATH = '../../swagger_documentation/userdata_endpoint'


class UserDataEndpoint(ApiBaseDefault):
    """/api/v1/userdata"""

    model = UserDataModel

    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/get_userdata.yml')
    def get(self):
        self.manager.log.info(
            'Set of all userdata objects where requested!'
        )

        try:
            getted = list(self.database.find(UserDataModel.TABLE))
            print(getted)
            return getted, 200
        except:
            return {'Request was not processed.'}, 400

    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/delete_all.yml')
    def delete(self):
        '''Deletes the entire userdata table.'''
        allUserData = self.get()  # Do a regular GET request to get all user progression.
        for data in allUserData[0]:
            UserDataByName.delete(self, username=data['user'])

        if len(allUserData[0]) == 0:
            return {"message": "There is no userdata in the database."}, 204
        else:
            return {"message": f"{len(allUserData[0])} userdata objects deleted"}, 200


class UserDataByName(ApiBase):

    # @protected
    @json_serialize
    def post(self, id_):
        ...

    # @protected
    @json_serialize
    def delete(self, username):
        delete_result = self.database.delete(
            UserDataModel.TABLE, user=username)

        if delete_result.deleted_count:
            return {"message": "ok"}
        return {"message": "nothing deleted"}, 204

    @json_serialize
    def get(self, username):
        getted = self.database.find_one(UserDataModel.TABLE, user=username)
        if getted:
            return getted, 200
        return {"message": "No user for this username"}, 204


endpoints = {
    "/api/v1/userdata": UserDataEndpoint,
    "/api/v1/userdata/<username>": UserDataByName
}

__slots__ = [endpoints]
