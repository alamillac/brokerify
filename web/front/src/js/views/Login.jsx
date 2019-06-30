import React from 'react';
import Logger from 'plugins/logger';
import LoginStores from 'stores/LoginStores';
import LoginActions from 'actions/LoginActions';
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';

const logger = Logger.createLogger('Login');

logger.info("Init view");

export default class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: ""
        };

    }

    componentDidMount() {
        this.login_store = LoginStores.listen(this._listener.bind(this));
    }

    componentWillUnmount() {
        this.login_store();
    }

    _listener(obj) {
        switch (obj.type) {
            case "LOGIN_ERROR":
                logger.info("Login error");
                //TODO show error
        }
    }

    _on_submit(event) {
        event.preventDefault();
        logger.info("Login submit");
        LoginActions.Login(this.state.username, this.state.password);
    }

    _on_email_change(event) {
        this.setState({username: event.target.value});
    }

    _on_password_change(event) {
        this.setState({password: event.target.value});
    }

    render() {
        return (
            <form onSubmit={this._on_submit.bind(this)}>
                <div className="container m-t-10vh">
                    <div className="col-xs-12 col-md-3 col-lg-3 col-md-offset-3 col-lg-offset-4">
                        <div className="col-sm-12 text-center m-b-lg">
                            <Input id="username" type="text" value={this.state.username} onChange={this._on_email_change.bind(this)} placeholder="Usuario"/>
                        </div>
                        <div className="col-sm-12 text-center m-b-lg">
                            <Input id="password" type="password" value={this.state.password} onChange={this._on_password_change.bind(this)} placeholder="Contraseña"/>
                        </div>
                        <div className="col-sm-12 text-center m-b-lg">
                            <Button variant="outlined" type="submit" className="btn" primary={true} label="Login" />
                        </div>
                    </div>
                </div>
            </form>
        );
    }
}
