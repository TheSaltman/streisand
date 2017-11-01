import * as React from 'react';
import { Store as ReduxStore } from 'redux';
import { Route, Redirect, RouterState, RedirectFunction } from 'react-router';

import Store from './store';

import App from './pages/App';
import Themes from './components/Themes';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/LoginPage';

import HomePage from './pages/HomePage';
import FilmPage from './pages/FilmPage';
import FilmsPage from './pages/FilmsPage';
import TorrentsPage from './pages/TorrentsPage';

export function createRoutes(store: ReduxStore<Store.All>) {
    function checkAuth(nextState: RouterState, replace: RedirectFunction) {
        const state = store.getState();
        if (!state.auth.isAuthenticated) {
            replace('/login');
        }
    }

    return (
        <div>
            <Redirect from="/" to="/home" />
            <Route path="/" component={App}>
                <Route path="/login" component={LoginPage} />
                <Route path="/about" component={AboutPage} />
                <Route path="/themes" component={Themes} />
                <Route onEnter={checkAuth}>
                    <Route path="/home" component={HomePage} />

                    <Route path="/films/:page" component={FilmsPage} />
                    <Redirect from="/films" to="/films/1" />
                    <Route path="/film/:filmId" component={FilmPage} />
                    <Redirect from="/film" to="/films/1" />

                    <Route path="/torrents/:page" component={TorrentsPage} />
                    <Redirect from="/torrents" to="/torrents/1" />
                </Route>
                <Redirect from="*" to="/home" />
            </Route>
        </div>
    );
}
