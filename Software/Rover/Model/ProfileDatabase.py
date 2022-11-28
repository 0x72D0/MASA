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
            self._profiles = list[Profile]()
    
    def get_profile(self, name: str) -> Profile:
        for profile in self._profiles:
            if profile.get_name() == name:
                return profile
        return None
    
    def get_profilesName(self) -> list[str]:
        names = list[str]()
        for profile in self._profiles:
            names.append(profile.get_name())
        return names
    
    def get_profileLen(self) -> int:
        return len(self._profiles)
    
    def save_profiles(self) -> None:
        with open(ProfileDatabase.PROFILE_FILENAME, "wb") as fd:
            pickle.dump(self._profiles, fd)
    
    def deleteProfile(self, name: str) -> None:
        for profile in self._profiles:
            if profile.get_name() == name:
                self._profiles.remove(profile)
                return
    
    def newProfile(self, name: str) -> None:
        self._profiles.append(Profile(name))