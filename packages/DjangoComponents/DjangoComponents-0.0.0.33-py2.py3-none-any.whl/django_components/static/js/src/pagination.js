var Pagebutton = React.createClass({
  pager: function() {
    if (this.props.clicky) {
      if (this.props.className.includes('ellipses')) {
        if (this.props.forward) this.props.forward();
        if (this.props.back) this.props.back();
      } else {
        this.props.clicky(this.props.children)
      }
    }
  },
  render: function() {
    var classes='page-button';
    if (this.props.page == this.props.children) classes+= ' active-page';
    return <span className={classes} onMouseDown={this.pager}>{this.props.children}</span>
  }
});

var Pagebar = React.createClass({
  render: function() {
    var items = [];
    if (this.props.pages > 1) {
      items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>1</Pagebutton>);

      if (this.props.pages <= 5) {
        for (var i = 2; i < this.props.pages; i++) {
          items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{i}</Pagebutton>);
        }
      } else {
        if (this.props.page < 4) {

          for (var i = 2; i < 5; i++) {
            items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{i}</Pagebutton>);
          }
          items.push(<Pagebutton className='page-button ellipses' forward={this.props.forward} clicky={this.props.clicky}>...</Pagebutton>);

        } else if (this.props.page >= this.props.pages - 2) {

          items.push(<Pagebutton className='page-button ellipses' back={this.props.back} clicky={this.props.clicky}>...</Pagebutton>);
          for (var i = this.props.pages - 3; i <= this.props.pages - 1; i++) {
            items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{i}</Pagebutton>);
          }

        } else if (this.props.page == 4) {
          for (var i = 2; i <= 5; i++) {
            items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{i}</Pagebutton>);
          }
          items.push(<Pagebutton className='page-button ellipses' back={this.props.back} clicky={this.props.clicky}>...</Pagebutton>);
        } else if (this.props.page == this.props.pages - 3) {
          items.push(<Pagebutton className='page-button ellipses' back={this.props.back} clicky={this.props.clicky}>...</Pagebutton>);
          for (var i = this.props.pages - 4; i <= this.props.pages - 1; i++) {
            items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{i}</Pagebutton>);
          }
        } else {

          items.push(<Pagebutton className='page-button ellipses' back={this.props.back} clicky={this.props.clicky}>...</Pagebutton>);
          for (var i = this.props.page - 2; i <= this.props.page + 2; i++) {
            items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{i}</Pagebutton>);
          }
          items.push(<Pagebutton className='page-button ellipses' forward={this.props.forward} clicky={this.props.clicky}>...</Pagebutton>);

        }
      }

      items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>{this.props.pages}</Pagebutton>);
    } else {
      items.push(<Pagebutton className='page-button' clicky={this.props.clicky} page={this.props.page}>1</Pagebutton>);
    }
    return <div className='pagebar-wrap'>{items}</div>;
  }
});

var Page = React.createClass({
  render: function() {
    var startPoint = ((this.props.page-1) * this.props.perPage);
    var endPoint = startPoint + this.props.perPage;
    var items = [];
    for (var i = startPoint; i < endPoint; i++) {
      if (typeof this.props.data[i] !== 'undefined') items.push(<div className='pagination-item'>{this.props.data[i]}</div>);
    }
    return (
      <div className='lk-pagination-content'>
        {items}
      </div>
    );
  }
});

var Pagination = React.createClass({
  getInitialState: function() {
    return {
      page: 1,  //cur page
      pages: Math.ceil(JSON.parse(this.props.data).length/this.props.perPage),  // num of pages
      data: JSON.parse(this.props.data),
      parsedData: JSON.parse(this.props.data),
      searchable: JSON.parse(this.props.searchable.toLowerCase()),
      search: ''
    };
  },
  changePage: function(num) {
    this.setState({page: parseInt(num)});
  },
  jumpBack: function() {
    this.setState({page: this.state.page - 3});
  },
  jumpForward: function() {
    this.setState({page: this.state.page + 3});
  },
  change: function(e) {
    this.setState({search: e.target.value.toLowerCase()});
    var curData = this.state.data;
    //var search = this.state.search;
    var newData = [];
    var search = e.target.value.split(' ');

    // old search...
    /*for (var i = 0; i < curData.length; i++) {
      if (curData[i].toLowerCase().includes(search) || search == '') newData.push(curData[i]);
      console.log(curData[i], search);
    }*/

    // fancy search...
    for (var i = 0; i < curData.length; i++) {

      var pushable = false;

      var amt = 0;

      for (var j = 0; j < search.length; j++) {
        if (curData[i].toLowerCase().includes(search[j]) || search[j] == '') {
          amt++;
        }
      }

      if (amt == search.length) pushable = true;

      if (pushable) {
        newData.push(curData[i]);
      }

    }

    console.log(Math.ceil(newData.length/this.props.perPage));

    this.setState({
      parsedData: newData,
      page: 1,
      pages: Math.ceil(newData.length/this.props.perPage)
    });
  },
  render: function() {
    var search = this.state.searchable ? (<input type='text' onChange={this.change} />) : '';
    return (
      <div className='lk-pagination'>
        {search}
        <Pagebar page={this.state.page} pages={this.state.pages} clicky={this.changePage} back={this.jumpBack} forward={this.jumpForward} />
        <Page page={this.state.page} data={this.state.parsedData} pages={this.state.pages} perPage={parseInt(this.props.perPage)} />
      </div>
    );
  }
});