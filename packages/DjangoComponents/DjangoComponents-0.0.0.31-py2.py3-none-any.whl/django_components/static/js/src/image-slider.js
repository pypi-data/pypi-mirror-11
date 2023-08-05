var ImageBarDot = React.createClass({
  update: function() {
    this.props.click(this.props.id);
  },
  render: function() {
    var classes = 'dot';
    if (this.props.id == this.props.imgOn) classes += ' dot-active';
    return (
      <span className={classes} onClick={this.update}></span>
    );
  }
});

var ImageSwitchBar = React.createClass({
  render: function() {
    var dots = [];
    for (var i = 0; i < this.props.amt; i++) {
      dots.push(<ImageBarDot click={this.props.click} id={i} imgOn={this.props.imgOn}></ImageBarDot>);
    }
    return (
      <div className='dot-holder'>{dots}</div>
    );
  }
});

var ImageHolder = React.createClass({
  render: function() {
    return (
      <img src={this.props.imgs[this.props.imgOn]} />
    );
  }
});

var ImageSlider = React.createClass({
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
      <div className='lk-image-slider'>
        <div className='arrow-left' onClick={this.prevImg}>&lt;</div><div className='arrow-right' onClick={this.nextImg}>&gt;</div>
        <ImageHolder imgs={this.state.imgs} imgOn={this.state.imgOn} />
        <ImageSwitchBar amt={this.state.imgs.length} click={this.switchImg} imgOn={this.state.imgOn} />
      </div>
    );
  }
});