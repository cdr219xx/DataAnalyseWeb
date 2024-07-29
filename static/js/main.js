class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
    };
  }

  componentDidMount() {
    fetch('/api/data')
      .then(response => response.json())
      .then(data => this.setState({ data }));
  }

  render() {
    const { data } = this.state;
    return (
      <div>
        <h1>Data Analysis Dashboard</h1>
        {data ? <p>{data.message}</p> : <p>Loading...</p>}
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
