import uuid

import requests
from decouple import config
from werkzeug.exceptions import InternalServerError


class WiseService:
    def __init__(self):
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        profile_id = self._get_profile_id()
        self.profile_id = profile_id

    def _get_profile_id(self):
        url = f"{self.main_url}/v1/profiles"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return [a["id"] for a in resp if a["type"] == "personal"][0]
        else:
            print(resp)
            return InternalServerError("Payment provider is not available at the moment")

    def create_quote(self, amount):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "targetAmount": amount,
        }
        resp = requests.post(url, json=data, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    def create_recipient_account(self, full_name, iban):
        url = f"{self.main_url}/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "legalType": "PRIVATE",
            "details": {"iban": iban},
        }
        resp = requests.post(url, json=data, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())

        url = f"{self.main_url}/v1/transfers"
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {}
        }
        # can be used for troubleshooting if any errors occur
        # requirements = requests.post(f"{self.main_url}/v1/transfer-requirements",
        #                              headers=self.headers, json=data)
        # print(requirements.json())
        resp = requests.post(url, json=data, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    def fund_transfer(self, transfer_id):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        resp = requests.post(url, headers=self.headers, json={"type": "BALANCE"})

        if resp.status_code == 201:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    def cancel_transfer(self, transfer_id):
        url = f"{self.main_url}/v1/transfers/{transfer_id}/cancel"
        resp = requests.put(url, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    # methods below this line for testing purpose only
    def create_balance_account(self, uuid: str, currency):
        """
        reference https://api-docs.wise.com/api-reference/balance#create
        to create balance for different currency. Change data where needed.
        """
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/balances"
        headers = self.headers
        headers["X-idempotence-uuid"] = uuid
        data = {
           "currency": currency,
           "type": "STANDARD"
         }

        resp = requests.post(url, headers=headers, json=data)

        if resp.status_code == 201:
            resp = resp.json()
            return resp
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    def get_balance_accounts_information(self):
        url = f"{self.main_url}//v4/profiles/{self.profile_id}/balances?types=STANDARD"
        header_needed = {"Authorization": f"Bearer {config('WISE_TOKEN')}"}
        resp = requests.get(url, headers=header_needed)
        return resp.json()

    def add_amount_to_balance_account(self, amount, currency):
        """
        reference https://api-docs.wise.com/api-reference/simulation#balance-top-up
        to fund your test balance accounts with desired amount
        """

        balance_info = self.get_balance_accounts_information()
        desired_account = [balance for balance in balance_info if balance["currency"] == currency][0]
        url = f"{self.main_url}/v1/simulation/balance/topup"
        data = {
              "profileId": self.profile_id,
              "balanceId": desired_account["id"],
              "currency": currency,
              "amount": amount
                }
        resp = requests.post(url, headers=self.headers, json=data)

        return resp


# uncomment below and change arguments as needed
# wise = WiseService()
# uuid = uuid.uuid4()
# wise.create_balance_account(str(uuid), "USD")
# wise.add_amount_to_balance_account(500, "EUR")

# if you need information about all of your transfers
# print(requests.get(f"https://api.sandbox.transferwise.tech/v1/transfers?profile={wise.profile_id}",
#                    headers={"Authorization": f"Bearer {config('WISE_TOKEN')}"}).json())
