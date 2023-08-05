var SearchOption = React.createClass({displayName: "SearchOption",
  update: function(e) {
    this.props.click(this.props.children);
  },
  render: function() {
    return React.createElement("div", {className: "search-suggestion", onMouseDown: this.update}, this.props.children);
  }
});

var DropdownSearch = React.createClass({displayName: "DropdownSearch",
  getInitialState: function() {
    return {update: this.props.click};
  },
  render: function() {
    var items = [];
    var click = this.props.click;
    var search = this.props.search.split(' ');
    var data = this.props.data;
    for (var i = 0; i < this.props.data.length; i++) {

      var pushable = false;

      var amt = 0;

      for (var j = 0; j < search.length; j++) {
        if (data[i].includes(search[j]) || search[j] == '') {
          amt++;
        }
      }

      if (amt == search.length) pushable = true;

      if (pushable) {
        items.push(this.props.data[i]);
      }

    }
    items = items.map(function(item) {return (React.createElement(SearchOption, {click: click},  item ))})
    return (
      React.createElement("div", {className: "dynamic-search-content", style: this.props.style}, 
         items 
      )
    );
  }
});

var CustomSearch = React.createClass({displayName: "CustomSearch",
  getInitialState: function() {
    return {
      search:'',
      showSuggestions:false,
      suggestionStyles:{display:'none'},
      searchId:0,
      data: JSON.parse(this.props.data),
      idData: (JSON.parse(this.props.data)).map(function(item){return item[0]}),
      nameData: (JSON.parse(this.props.data)).map(function(item){return item[1]})
    };
  },
  change: function(e) {
    this.setState({search: e.target.value});
  },
  focus: function() {
    this.setState({suggestionStyles:{display:'block'}});
  },
  blur: function(e) {
    this.setState({suggestionStyles:{display:'none'}});
  },
  clickSuggestion: function(item) {
    this.setState({
      search: item,
      searchId: this.state.idData[this.state.nameData.indexOf(item)]
    });
    this.blur();
  },
  render: function() {
    if (!(this.props.data)) {
      throw "Please pass CustomSearch some data!";
    }
    console.log(this.state.nameData)
    return (
      React.createElement("div", {className: "lk-dynamic-search"}, 
        React.createElement("input", {type: "text", onChange: this.change, onFocus: this.focus, onBlur: this.blur, value: this.state.search}), 
        React.createElement("input", {type: "text", name: this.props.name, value: this.state.searchId, style: {display:'none'}}), 
        React.createElement(DropdownSearch, {data: this.state.nameData, search: this.state.search, click: this.clickSuggestion, style: this.state.suggestionStyles})
      )
    );
  }
});