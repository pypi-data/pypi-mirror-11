var Alert = React.createClass({displayName: "Alert",
	remove: function() {
		React.unmountComponentAtNode(document.getElementById(this.props.container));
	},
	render: function() {
		var classes = 'lk-alert alert-' + this.props.type;  //success, info, warning, danger
		var closeButton = JSON.parse(this.props.closable.toLowerCase()) ? React.createElement("span", {onClick: this.remove, className: "remove-alert"}, "x") : '';
		return (
			React.createElement("div", {className: classes}, 
				React.createElement("span", {dangerouslySetInnerHTML: {__html: this.props.content}}), 
				closeButton
			)
		);
	}
});