r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Trusthub
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Any, Dict, Optional, Union
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version


class ComplianceInquiriesInstance(InstanceResource):
    """
    :ivar inquiry_id: The unique ID used to start an embedded compliance registration session.
    :ivar inquiry_session_token: The session token used to start an embedded compliance registration session.
    :ivar customer_id: The CustomerID matching the Customer Profile that should be resumed or resubmitted for editing.
    :ivar url: The URL of this resource.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        customer_id: Optional[str] = None,
    ):
        super().__init__(version)

        self.inquiry_id: Optional[str] = payload.get("inquiry_id")
        self.inquiry_session_token: Optional[str] = payload.get("inquiry_session_token")
        self.customer_id: Optional[str] = payload.get("customer_id")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "customer_id": customer_id or self.customer_id,
        }
        self._context: Optional[ComplianceInquiriesContext] = None

    @property
    def _proxy(self) -> "ComplianceInquiriesContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: ComplianceInquiriesContext for this ComplianceInquiriesInstance
        """
        if self._context is None:
            self._context = ComplianceInquiriesContext(
                self._version,
                customer_id=self._solution["customer_id"],
            )
        return self._context

    def update(
        self, primary_profile_sid: str, theme_set_id: Union[str, object] = values.unset
    ) -> "ComplianceInquiriesInstance":
        """
        Update the ComplianceInquiriesInstance

        :param primary_profile_sid: The unique SID identifier of the Primary Customer Profile that should be used as a parent. Only necessary when creating a secondary Customer Profile.
        :param theme_set_id: Theme id for styling the inquiry form.

        :returns: The updated ComplianceInquiriesInstance
        """
        return self._proxy.update(
            primary_profile_sid=primary_profile_sid,
            theme_set_id=theme_set_id,
        )

    async def update_async(
        self, primary_profile_sid: str, theme_set_id: Union[str, object] = values.unset
    ) -> "ComplianceInquiriesInstance":
        """
        Asynchronous coroutine to update the ComplianceInquiriesInstance

        :param primary_profile_sid: The unique SID identifier of the Primary Customer Profile that should be used as a parent. Only necessary when creating a secondary Customer Profile.
        :param theme_set_id: Theme id for styling the inquiry form.

        :returns: The updated ComplianceInquiriesInstance
        """
        return await self._proxy.update_async(
            primary_profile_sid=primary_profile_sid,
            theme_set_id=theme_set_id,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Trusthub.V1.ComplianceInquiriesInstance {}>".format(context)


class ComplianceInquiriesContext(InstanceContext):

    def __init__(self, version: Version, customer_id: str):
        """
        Initialize the ComplianceInquiriesContext

        :param version: Version that contains the resource
        :param customer_id: The unique CustomerId matching the Customer Profile/Compliance Inquiry that should be resumed or resubmitted. This value will have been returned by the initial Compliance Inquiry creation call.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "customer_id": customer_id,
        }
        self._uri = "/ComplianceInquiries/Customers/{customer_id}/Initialize".format(
            **self._solution
        )

    def update(
        self, primary_profile_sid: str, theme_set_id: Union[str, object] = values.unset
    ) -> ComplianceInquiriesInstance:
        """
        Update the ComplianceInquiriesInstance

        :param primary_profile_sid: The unique SID identifier of the Primary Customer Profile that should be used as a parent. Only necessary when creating a secondary Customer Profile.
        :param theme_set_id: Theme id for styling the inquiry form.

        :returns: The updated ComplianceInquiriesInstance
        """
        data = values.of(
            {
                "PrimaryProfileSid": primary_profile_sid,
                "ThemeSetId": theme_set_id,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return ComplianceInquiriesInstance(
            self._version, payload, customer_id=self._solution["customer_id"]
        )

    async def update_async(
        self, primary_profile_sid: str, theme_set_id: Union[str, object] = values.unset
    ) -> ComplianceInquiriesInstance:
        """
        Asynchronous coroutine to update the ComplianceInquiriesInstance

        :param primary_profile_sid: The unique SID identifier of the Primary Customer Profile that should be used as a parent. Only necessary when creating a secondary Customer Profile.
        :param theme_set_id: Theme id for styling the inquiry form.

        :returns: The updated ComplianceInquiriesInstance
        """
        data = values.of(
            {
                "PrimaryProfileSid": primary_profile_sid,
                "ThemeSetId": theme_set_id,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return ComplianceInquiriesInstance(
            self._version, payload, customer_id=self._solution["customer_id"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Trusthub.V1.ComplianceInquiriesContext {}>".format(context)


class ComplianceInquiriesList(ListResource):

    def __init__(self, version: Version):
        """
        Initialize the ComplianceInquiriesList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/ComplianceInquiries/Customers/Initialize"

    def create(
        self,
        primary_profile_sid: str,
        notification_email: Union[str, object] = values.unset,
        theme_set_id: Union[str, object] = values.unset,
    ) -> ComplianceInquiriesInstance:
        """
        Create the ComplianceInquiriesInstance

        :param primary_profile_sid: The unique SID identifier of the Primary Customer Profile that should be used as a parent. Only necessary when creating a secondary Customer Profile.
        :param notification_email: The email address that approval status updates will be sent to. If not specified, the email address associated with your primary customer profile will be used.
        :param theme_set_id: Theme id for styling the inquiry form.

        :returns: The created ComplianceInquiriesInstance
        """

        data = values.of(
            {
                "PrimaryProfileSid": primary_profile_sid,
                "NotificationEmail": notification_email,
                "ThemeSetId": theme_set_id,
            }
        )
        headers = values.of({"Content-Type": "application/x-www-form-urlencoded"})

        payload = self._version.create(
            method="POST", uri=self._uri, data=data, headers=headers
        )

        return ComplianceInquiriesInstance(self._version, payload)

    async def create_async(
        self,
        primary_profile_sid: str,
        notification_email: Union[str, object] = values.unset,
        theme_set_id: Union[str, object] = values.unset,
    ) -> ComplianceInquiriesInstance:
        """
        Asynchronously create the ComplianceInquiriesInstance

        :param primary_profile_sid: The unique SID identifier of the Primary Customer Profile that should be used as a parent. Only necessary when creating a secondary Customer Profile.
        :param notification_email: The email address that approval status updates will be sent to. If not specified, the email address associated with your primary customer profile will be used.
        :param theme_set_id: Theme id for styling the inquiry form.

        :returns: The created ComplianceInquiriesInstance
        """

        data = values.of(
            {
                "PrimaryProfileSid": primary_profile_sid,
                "NotificationEmail": notification_email,
                "ThemeSetId": theme_set_id,
            }
        )
        headers = values.of({"Content-Type": "application/x-www-form-urlencoded"})

        payload = await self._version.create_async(
            method="POST", uri=self._uri, data=data, headers=headers
        )

        return ComplianceInquiriesInstance(self._version, payload)

    def get(self, customer_id: str) -> ComplianceInquiriesContext:
        """
        Constructs a ComplianceInquiriesContext

        :param customer_id: The unique CustomerId matching the Customer Profile/Compliance Inquiry that should be resumed or resubmitted. This value will have been returned by the initial Compliance Inquiry creation call.
        """
        return ComplianceInquiriesContext(self._version, customer_id=customer_id)

    def __call__(self, customer_id: str) -> ComplianceInquiriesContext:
        """
        Constructs a ComplianceInquiriesContext

        :param customer_id: The unique CustomerId matching the Customer Profile/Compliance Inquiry that should be resumed or resubmitted. This value will have been returned by the initial Compliance Inquiry creation call.
        """
        return ComplianceInquiriesContext(self._version, customer_id=customer_id)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Trusthub.V1.ComplianceInquiriesList>"
