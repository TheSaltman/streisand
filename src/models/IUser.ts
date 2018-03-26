
export interface IPartialUser {
    id: number;
    username: string;
}

interface IUser {
    accountStatus: string;
    avatarUrl: string;
    customTitle: string;
    id: number;
    isDonor: boolean;
    userClass: string;
    username: string;
}

export default IUser;