import React from 'react';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import './App.css';
import Article from './components/Article';
import ArticlePreview from './components/ArticlePreview';
import Layout from './components/Layout';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
	  <Route path="/" element={<ArticlePreview />} />
	  <Route path="/article/:id" element={<Article filePath="/articles" />} />
	</Routes>
      </Layout>
    </Router>
  )
}

export default App
