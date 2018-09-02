import React from 'react';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Logger from 'plugins/logger';

const logger = Logger.createLogger('CollapsedSection');

logger.info("Init view");

export default class CollapsedSection extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
        };

    }

    render() {
        return (
            <ExpansionPanel defaultExpanded={this.props.expanded}>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>{this.props.title}</Typography>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    {this.props.children}
                </ExpansionPanelDetails>
            </ExpansionPanel>
        );
    }
}
