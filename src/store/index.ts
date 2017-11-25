import { RouterState } from 'react-router-redux';

import IFilm from '../models/IFilm';
import IAuthInfo from '../models/IAuthInfo';
import IDeviceInfo from '../models/IDeviceInfo';
import ILocationInfo from '../models/ILocationInfo';
import ITorrentItemSet from '../models/ITorrentItemSet';
import IPagedItemSet from '../models/base/IPagedItemSet';

namespace Store {
    export type Films = IPagedItemSet<IFilm>;
    export type Torrents = ITorrentItemSet;

    export type Errors = {
        authError: string;
        unkownError: string;
    };

    export type All = {
        errors: Errors;
        routing: RouterState;
        location: ILocationInfo;
        auth: IAuthInfo;
        films: Films;
        torrents: Torrents;
        deviceInfo: IDeviceInfo;
    };
}

export default Store;
