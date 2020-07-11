import { Route, BrowserRouter as Router, Switch } from "react-router-dom";
import Dashboard from "components/Dashboard";
import React from "react";

const App = () => (
  <Router>
    <Switch>
      <Route exact path="/">
        <Dashboard />
      </Route>
    </Switch>
  </Router>
);

export default App;
