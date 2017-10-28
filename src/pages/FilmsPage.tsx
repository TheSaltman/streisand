import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import globals from '../utilities/globals';
import { getFilms } from '../actions/FilmsAction';
import FilmsView from '../components/films/FilmsView';

export type Props = {
    params: {
        page: string;
    };
};

type ConnectedState = {
    page: number;
    isLoading: boolean;
};

type ConnectedDispatch = {
    getFilms: (page: number) => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class FilmsPage extends React.Component<CombinedProps> {
    public componentWillMount() {
        if (!this.props.isLoading) {
            this.props.getFilms(this.props.page);
        }
    }

    public componentWillReceiveProps(props: CombinedProps) {
        if (!props.isLoading && props.page !== this.props.page) {
            this.props.getFilms(props.page);
        }
    }

    public render() {
        return (
            <FilmsView page={this.props.page} />
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const pageNumber = Number((ownProps.params && ownProps.params.page) || 1);
    const page = state.films.pages[pageNumber];
    return {
        page: pageNumber,
        isLoading: page ? page.loading : false
    };
};

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getFilms: (page: number) => dispatch(getFilms(page))
});

export default connect(mapStateToProps, mapDispatchToProps)(FilmsPage);
