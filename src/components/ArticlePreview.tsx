import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./ArticlePreview.css";

interface ArticleMeta {
  id: string;
  title: string;
  excerpt: string;
}

const ArticlePreview: React.FC = () => {
  const [articles, setArticles] = useState<ArticleMeta[]>([]);

  useEffect(() => {
    fetch("/articles/articleList.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch the article list");
        }
        return response.json();
      })
      .then((data) => setArticles(data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="ArticlePreview">
      <h1>Teague Lasser</h1>
			<h2>Engineer, Philosopher, Dreamer</h2>
      {articles.map((article) => (
        <div key={article.id} className="ArticleItem">
          <Link to={`/article/${article.id}`}>
            <h2>{article.title}</h2>
          </Link>
          <p>{article.excerpt}</p>
        </div>
      ))}
    </div>
  );
};

export default ArticlePreview;
