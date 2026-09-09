# ---------------------------------------------- #
# Example AnonyMate symmetric encryption wrapper #
# Replace with your actual AnonyMate Implementation if available. #
# ---------------------------------------------- #

import json
from cryptography.fernet import Fernet

class AnonyMate:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt (self, data):
        """
        Accepts a python object and returns encrypted bytes
        """
        payload = json.dumps(data, default=str). encode("utf-8")
        return self.cipher.encrypt(payload)

    def decrypt (self, encrypted_data):
        """
        Returns the original Python object.
        """
        payload = self.cipher.decrypt(encrypted_data)
        return json.loads(payload.decode("utf-8"))

# -----------------------------
# Profile Manager
# -----------------------------

class ProfileManager:
    ALLOWED_FIELDS = {
        "name",
        "birthdate"
        "sex",
        "blood_type"
    }

    def __init__(self, profiles):
        self.profiles = profiles
        self.anonymizer = AnonyMate()
        self.encrypted_profiles = None

    def encrypt_profiles(self):
        """
        Encrypt all profile data upon user request.
        """
        self.encrypted_profiles = self.anonymizer.encrypt(self.profiles)
        print("Profiles encrypted successfully.")

    def decrypt_profiles(selfself):
        """
        Decrypt profile data for querying.
        """
        if self.encrypted_profiles is None:
            return self.profiles

        return self.anonymizer.decrypt(self.encrypted_profiles)

    def query_profile(selfself, name, field):
        """
        Query a limited set of allowed fields.
        """
        if field not in self.ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{field}' is not allowed."
                f"Allowed fields: {",".join(sorted(self.ALLOWED_FIELDS))}"
            )

        profiles = self.decrypt_profiles()

        for profile in profiles:
            if profile["name"].lower() == name.lower():
                return {
                    "name": profile["name"],
                    field: profile.get(field)
                }
        return {"error": "Profile not found"}