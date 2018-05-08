
import ErrorAction from '../../ErrorAction';
import { transformTopic } from '../transforms';
import { fetchData } from '../../ActionHelper';
import { ThunkAction } from '../../ActionTypes';
import globals from '../../../utilities/globals';
import { get } from '../../../utilities/Requestor';
import IPagedResponse from '../../../models/base/IPagedResponse';
import { IForumGroupData } from '../../../models/forums/IForumGroup';
import { IForumThreadResponse } from '../../../models/forums/IForumThread';

type Response = IPagedResponse<IForumThreadResponse>;

export type ForumTopicReceivedAction = {
    type: 'RECEIVED_FORUM_TOPIC',
    id: number,
    page: number,
    count: number,
    data: IForumGroupData
};
type ForumTopicAction =
    { type: 'FETCHING_FORUM_TOPIC', id: number, page: number } |
    ForumTopicReceivedAction |
    { type: 'FAILED_FORUM_TOPIC', id: number, page: number } |
    { type: 'INVALIDATE_FORUM_TOPIC', id: number, page: number };
export default ForumTopicAction;
type Action = ForumTopicAction | ErrorAction;

type Props = {
    id: number;
    page: number;
};

function fetching(props: Props): Action {
    return { type: 'FETCHING_FORUM_TOPIC', id: props.id, page: props.page };
}

function received(props: Props, response: Response): Action {
    return {
        type: 'RECEIVED_FORUM_TOPIC',
        id: props.id,
        page: props.page,
        count: response.count,
        data: transformTopic(response)
    };
}

function failure(props: Props): Action {
    return { type: 'FAILED_FORUM_TOPIC', id: props.id, page: props.page };
}

export function invalidate(props: Props) {
    return { type: 'INVALIDATE_FORUM_TOPIC', id: props.id, page: props.page };
}

export function getThreads(id: number, page: number = 1): ThunkAction<Action> {
    const errorPrefix = `Fetching page ${page} of the forum topic (${id}) failed`;
    return fetchData({ request, fetching, received, failure, errorPrefix, props: { id, page } });
}

function request(token: string, props: Props): Promise<Response> {
    return get({ token, url: `${globals.apiUrl}/forum-thread-index/?topic_id=${props.id}&page=${props.page}` });
}