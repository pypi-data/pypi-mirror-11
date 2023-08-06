class Metaflows:
    """  2600hz Kazoo Metaflows API.

        :param rest_request: The request client to use.
            (optional, default: pykazoo.RestRequest())
        :type rest_request: pykazoo.restrequest.RestRequest
    """

    def __init__(self, rest_request):
        self.rest_request = rest_request

    def get_account_metaflows(self, account_id):
        """ Get Metaflows for an Account.

        :param account_id: ID of Account to get Metaflows for.
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :rtype: dict
        """
        return self.rest_request.get('accounts/' + str(account_id) +
                                     '/metaflows', None)

    def get_callflow_metaflows(self, account_id, callflow_id):
        """ Get Metaflows for a Callflow.

        :param account_id: ID of Account to get Metaflows for.
        :param callflow_id: ID of Callflow to get Metaflows for.
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type callflow_id: str
        :rtype: dict
        """
        return self.rest_request.get('accounts/' + str(account_id) +
                                     '/callflows/' + str(callflow_id) +
                                     '/metaflows', None)

    def get_device_metaflows(self, account_id, device_id):
        """ Get Metaflows for a Device.

        :param account_id: ID of Account to get Metaflows for.
        :param device_id: ID of Device to get Metaflows for.
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type device_id: str
        :rtype: dict
        """
        return self.rest_request.get('accounts/' + str(account_id) +
                                     '/devices/' + str(device_id) +
                                     '/metaflows', None)

    def update_account_metaflows(self, account_id, data):
        """ Updates Metaflows for an Account

        :param account_id: ID of Account to update Metaflows for.
        :param data: Kazoo Account data (see official API Docs).
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type data: dict
        :rtype: dict
        """
        return self.rest_request.post('accounts/' + str(account_id) +
                                      '/metaflows', data)

    def update_callflow_metaflows(self, account_id, callflow_id, data):
        """ Updates Metaflows for a Callflow

        :param account_id: ID of Account to update Metaflows for.
        :param callflow_id: ID of Callflow to update Metaflows for.
        :param data: Kazoo Account data (see official API Docs).
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type callflow_id: str
        :type data: dict
        :rtype: dict
        """
        return self.rest_request.post('accounts/' + str(account_id) +
                                      '/callflows/' + str(callflow_id) +
                                      '/metaflows', data)

    def update_device_metaflows(self, account_id, device_id, data):
        """ Updates Metaflows for a Device

        :param account_id: ID of Account to update Metaflows for.
        :param device_id: ID of Device to update Metaflows for.
        :param data: Kazoo Account data (see official API Docs).
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type device_id: str
        :type data: dict
        :rtype: dict
        """
        return self.rest_request.post('accounts/' + str(account_id) +
                                      '/devices/' + str(device_id) +
                                      '/metaflows', data)

    def delete_account_metaflows(self, account_id):
        """ Deletes Metaflows for an Account

        :param account_id: ID of Account to delete Metaflows for.
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :rtype: dict
        """
        return self.rest_request.delete('accounts/' + str(account_id) +
                                        '/metaflows')

    def delete_callflow_metaflows(self, account_id, callflow_id):
        """ Deletes Metaflows for a Callflow

        :param account_id: ID of Account to delete Metaflows for.
        :param callflow_id: ID of Callflow to delete Metaflows for.
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type callflow_id: str
        :rtype: dict
        """
        return self.rest_request.delete('accounts/' + str(account_id) +
                                        '/callflows/' + str(callflow_id) +
                                        '/metaflows')

    def delete_device_metaflows(self, account_id, device_id):
        """ Deletes Metaflows for a Device

        :param account_id: ID of Account to delete Metaflows for.
        :param device_id: ID of Device to delete Metaflows for.
        :return: Kazoo Data (see official API docs).
        :type account_id: str
        :type device_id: str
        :rtype: dict
        """
        return self.rest_request.delete('accounts/' + str(account_id) +
                                        '/devices/' + str(device_id) +
                                        '/metaflows')
