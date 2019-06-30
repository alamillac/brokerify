import React from 'react';
import Logger from 'plugins/logger';

const styles = {
    margin: '30px',
};

export default class Portfolio extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            indices: [],
            stocks: [],
        };
    }

    componentDidMount() {}

    componentWillUnmount() {}

    _stock_listener(response) {}

    render() {
        return <div style={styles}></div>;
    }
}
