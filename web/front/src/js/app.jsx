import Logger from 'plugins/logger';
import React from 'react';
import Reflux from 'reflux';
import Login from 'views/Login.jsx';
import Home from 'views/Home/Home.jsx';
import Portfolio from 'views/Portfolio/Portfolio.jsx';
import Header from 'components/Header.jsx';
import LoginStores from 'stores/LoginStores';
import {
    Router,
    Switch,
    BrowserRouter,
    Route,
    Redirect,
    Link,
} from 'react-router-dom';

const logger = Logger.createLogger('App');

logger.info('Init app component');

export default class App extends Reflux.Component {
    constructor(props) {
        super(props);
        const user = JSON.parse(sessionStorage.getItem('user'));
        this.state = {
            user: user,
        };
    }

    componentDidMount() {
        LoginStores.listen(this._login_store_listener.bind(this));
    }

    _login_store_listener(loginResponse) {
        switch (loginResponse.type) {
            case 'LOGIN_OK':
                logger.info('Login ok');
                const strUser = JSON.stringify(loginResponse.data);
                sessionStorage.setItem('user', strUser);
                this.setState({
                    user: loginResponse.data,
                });
                break;
            case 'LOGOUT_OK':
                logger.info('Logout ok');
                sessionStorage.removeItem('user');
                this.setState({
                    user: null,
                });
                break;
            case 'LOGIN_ERROR':
                logger.info('Login error');
                sessionStorage.removeItem('user');
                this.setState({
                    user: null,
                });
                break;
        }
    }

    _user_is_logged() {
        logger.info('User is logged?');
        if (this.state.user) {
            return true;
        }
        return false;
    }

    _login_page() {
        if (!this._user_is_logged()) {
            return (
                <main>
                    <Login />
                </main>
            );
        } else {
            return <Redirect to="/home" />;
        }
    }

    _home() {
        if (this._user_is_logged()) {
            return (
                <main>
                    <Header user={this.state.user} section="Home" />
                    <Home user={this.state.user} />
                </main>
            );
        } else {
            return <Redirect to="/login" />;
        }
    }

    _portfolio({match}) {
        if (this._user_is_logged()) {
            const portfolioId = match.params.portfolioId;

            //TODO get details from portfolio (Stocks...)
            return (
                <main>
                    <Header user={this.state.user} section="Home" />
                    <Portfolio user={this.state.user} />
                </main>
            );
        } else {
            return <Redirect to="/login" />;
        }
    }

    render() {
        return (
            <Switch>
                <Route exact path="/" render={props => this._login_page()} />
                <Route
                    exact
                    path="/login"
                    render={props => this._login_page()}
                />
                <Route exact path="/home" render={props => this._home()} />
                <Route
                    path="/portfolio/:portfolioId"
                    render={props => this._portfolio(props)}
                />
                <Route
                    path="*"
                    exact={true}
                    render={props => <Redirect to="/" />}
                />
            </Switch>
        );
    }
}
