var SearchOption = React.createClass({
  update: function(e) {
    this.props.click(this.props.children);
  },
  render: function() {
    return <div className='search-suggestion' onMouseDown={this.update}>{this.props.children}</div>;
  }
});

var DropdownSearch = React.createClass({
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
    items = items.map(function(item) {return (<SearchOption click={click}>{ item }</SearchOption>)})
    return (
      <div className='dynamic-search-content' style={this.props.style}>
        { items }
      </div>
    );
  }
});

var CustomSearch = React.createClass({
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
      <div className='lk-dynamic-search'>
        <input type='text' onChange={this.change} onFocus={this.focus} onBlur={this.blur} value={this.state.search} />
        <input type='text' name={this.props.name} value={this.state.searchId} style={{display:'none'}} />
        <DropdownSearch data={this.state.nameData} search={this.state.search} click={this.clickSuggestion} style={this.state.suggestionStyles} />
      </div>
    );
  }
});