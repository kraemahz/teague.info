import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./ArticlePreview.css";

interface ArticleMeta {
    id: string;
    title: string;
    excerpt: string;
    image: string;
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
            <p className="subtitle">Engineer, Philosopher, Dreamer</p>

            <h3 className="section-title">Papers</h3>
            <a href="/papers/gfm/" className="paper-link">
                <p className="paper-title">Goal-Frontier Maximizers are Civilization Aligned</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>

            <h3 className="section-title">Writing</h3>
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
