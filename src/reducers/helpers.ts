import * as objectAssign from 'object-assign';
import { combineReducers as combine, Reducer } from 'redux';

// This type change has already been made in redux and will be in v4
// However, we don't know when that will be release.
// So we will use it via this passthrough until then.
export type ReducersMapObject<S> = {
    [K in keyof S]: Reducer<S[K]>;
};

export function combineReducers<S>(reducers: ReducersMapObject<S>): Reducer<S> {
    return combine(reducers);
}

type SimpleItem = { id: number; };
type ItemMap<T extends SimpleItem> = { [id: number]: T };
export function mergeItem<T extends SimpleItem>(map: ItemMap<T>, item: T) {
    if (map[item.id]) {
        map[item.id] = objectAssign({}, map[item.id], item);
    } else {
        map[item.id] = item;
    }
}