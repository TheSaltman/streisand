import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import ITorrent from '../../models/ITorrent';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

type TorrentAction =
    { type: 'FETCHING_TORRENT', id: number } |
    { type: 'RECEIVED_TORRENT', torrent: ITorrent } |
    { type: 'TORRENT_FAILURE', id: number };
export default TorrentAction;
type Action = TorrentAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_TORRENT', id };
}

function received(response: ITorrent): Action {
    return {
        type: 'RECEIVED_TORRENT',
        torrent: response
    };
}

function failure(id: number): Action {
    return { type: 'TORRENT_FAILURE', id };
}

export function getTorrent(id: number): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return fetch(state.auth.token, id).then((response: ITorrent) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number): Promise<ITorrent> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/torrents/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}