import pickle
import os

from Model.Profile import Profile

class ProfileDatabase:
    PROFILE_FILENAME = "profiles.pkl"

    def __init__(self) -> None:
        if os.path.exists(ProfileDatabase.PROFILE_FILENAME):
            with open(ProfileDatabase.PROFILE_FILENAME, "rb") as fd:
                self._profiles = pickle.load(fd)
        else:
            self._profiles = []
    
    def get_profile(self, name: str) -> Profile:
        for profile in self._profiles:
            if profile.get_name() == name:
                return profile
        return None
    
    def get_profilesName(self) -> list:
        names = []
        for profile in self._profiles:
            names.append(profile.get_name())
        return names
    
    def get_profileLen(self) -> int:
        return len(self._profiles)
    
    def save_profiles(self):
        with open(ProfileDatabase.PROFILE_FILENAME, "wb") as fd:
            pickle.dump(self._profiles, fd)
    
    def newProfile(self, name: str):
        self._profiles.append(Profile(name))