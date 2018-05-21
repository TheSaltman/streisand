import * as objectAssign from 'object-assign';

import Action from '../actions/torrents';
import ITorrent from '../models/ITorrent';
import { combineReducers } from './helpers';
import { getPageReducer } from './utilities/page';
import ITorrentItemSet from '../models/ITorrentItemSet';
import { IPage, INodeMap } from '../models/base/IPagedItemSet';
import { addLoadedNode, addLoadedNodes, markLoading, markFailed } from './utilities/mutations';

type ItemMap = INodeMap<ITorrent>;
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'REQUEST_TORRENT':
            return markLoading(state, action.props.id);
        case 'RECEIVED_TORRENT':
            return addLoadedNode(state, action.torrent);
        case 'FAILED_TORRENT':
            return markFailed(state, action.props.id);
        case 'RECEIVED_TORRENTS':
        case 'RECEIVED_FILM_TORRENTS':
            return addLoadedNodes(state, action.props.items);
        default:
            return state;
    }
}

const pageReducer = getPageReducer('TORRENTS');
type Pages = { [page: number]: IPage };
function pages(state: Pages = {}, action: Action): Pages {
    switch (action.type) {
        case 'REQUEST_TORRENTS':
        case 'RECEIVED_TORRENTS':
        case 'FAILED_TORRENTS':
            const page: IPage = pageReducer(state[action.props.page], action);
            return objectAssign({}, state, { [action.props.page]: page });
        default:
            return state;
    }
}

const filmPageReducer = getPageReducer('FILM_TORRENTS');
type Torrents = { [id: number]: IPage };
function byFilmId(state: Torrents = {}, action: Action): Torrents {
    switch (action.type) {
        case 'REQUEST_FILM_TORRENTS':
        case 'RECEIVED_FILM_TORRENTS':
        case 'FAILED_FILM_TORRENTS':
            const page: IPage = filmPageReducer(state[action.props.page], action);
            return objectAssign({}, state, { [action.props.page]: page });
        default:
            return state;
    }
}

function pageSize(state: number = 0, action: Action): number {
    switch (action.type) {
        // TODO: Split this up
        case 'RECEIVED_TORRENTS':
        case 'RECEIVED_FILM_TORRENTS':
            return action.props.pageSize;
        default:
            return state;
    }
}

function count(state: number = 0, action: Action): number {
    switch (action.type) {
        case 'RECEIVED_TORRENTS':
            return action.props.count;
        default:
            return state;
    }
}

export default combineReducers<ITorrentItemSet>({ byId, byFilmId, pageSize, count, pages });