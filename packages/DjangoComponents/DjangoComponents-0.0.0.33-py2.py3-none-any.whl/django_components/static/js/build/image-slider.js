var ImageBarDot = React.createClass({displayName: "ImageBarDot",
  update: function() {
    this.props.click(this.props.id);
  },
  render: function() {
    var classes = 'dot';
    if (this.props.id == this.props.imgOn) classes += ' dot-active';
    return (
      React.createElement("span", {className: classes, onClick: this.update})
    );
  }
});

var ImageSwitchBar = React.createClass({displayName: "ImageSwitchBar",
  render: function() {
    var dots = [];
    for (var i = 0; i < this.props.amt; i++) {
      dots.push(React.createElement(ImageBarDot, {click: this.props.click, id: i, imgOn: this.props.imgOn}));
    }
    return (
      React.createElement("div", {className: "dot-holder"}, dots)
    );
  }
});

var ImageHolder = React.createClass({displayName: "ImageHolder",
  render: function() {
    return (
      React.createElement("img", {src: this.props.imgs[this.props.imgOn]})
    );
  }
});

var ImageSlider = React.createClass({displayName: "ImageSlider",
  getInitialState: function() {
    return {
      imgs:JSON.parse(this.props.imgs),
      imgOn:0
    };
  },
  switchImg: function(num) {
    this.setState({imgOn:num});
  },
  prevImg: function() {
    if (this.state.imgOn === 0) {
      this.setState({imgOn: this.state.imgs.length - 1});
    } else {
      this.setState({imgOn: this.state.imgOn - 1});
    }
  },
  nextImg: function() {
    if (this.state.imgOn === this.state.imgs.length - 1) {
      this.setState({imgOn: 0});
    } else {
      this.setState({imgOn: this.state.imgOn + 1});
    }
  },
  render: function() {
    return (
      React.createElement("div", {className: "lk-image-slider"}, 
        React.createElement("div", {className: "arrow-left", onClick: this.prevImg}, "<"), React.createElement("div", {className: "arrow-right", onClick: this.nextImg}, ">"), 
        React.createElement(ImageHolder, {imgs: this.state.imgs, imgOn: this.state.imgOn}), 
        React.createElement(ImageSwitchBar, {amt: this.state.imgs.length, click: this.switchImg, imgOn: this.state.imgOn})
      )
    );
  }
});