var Alert = React.createClass({
	remove: function() {
		React.unmountComponentAtNode(document.getElementById(this.props.container));
	},
	render: function() {
		var classes = 'lk-alert alert-' + this.props.type;  //success, info, warning, danger
		var closeButton = JSON.parse(this.props.closable.toLowerCase()) ? <span onClick={this.remove} className='remove-alert'>x</span> : '';
		return (
			<div className={classes}>
				<span dangerouslySetInnerHTML={{__html: this.props.content}} />
				{closeButton}
			</div>
		);
	}
});