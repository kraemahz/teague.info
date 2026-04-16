import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./ArticlePreview.css";

interface ArticleMeta {
    id: string;
    title: string;
    excerpt: string;
    image: string;
    date: string;
}

function formatDate(iso: string): string {
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
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
            .then((data: ArticleMeta[]) =>
                setArticles(data.sort((a, b) =>
                    new Date(b.date).getTime() - new Date(a.date).getTime()
                ))
            )
            .catch((error) => console.error(error));
    }, []);

    return (
        <div className="ArticlePreview">
            <h1>Teague Lasser</h1>
            <p className="subtitle">Engineer, Philosopher, Dreamer</p>

            <h3 className="section-title">Papers</h3>
            <a href="/papers/wamura/" className="paper-link">
                <p className="paper-title">Controlled Relaxation Protocols for the Wamura Problem</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>
            <a href="/papers/phase/" className="paper-link">
                <p className="paper-title">Cross-Substrate Channel Redundancy Governs Monopolar Convergence</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>
            <a href="/papers/exo/" className="paper-link">
                <p className="paper-title">Exogenous Verification for Alignment</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>
            <a href="/papers/scm/" className="paper-link">
                <p className="paper-title">A Structural Causal Model for Goal-Frontier Maximization</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>
            <a href="/papers/horizon/" className="paper-link">
                <p className="paper-title">Horizon-Aware Goal-Frontier Maximization and the Anti-Monopolar Property</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>
            <a href="/papers/poset/" className="paper-link">
                <p className="paper-title">Computable Goal Frontiers and the Gradient Toward Civilization-Building</p>
                <p className="paper-meta">2026 · Lasser, Claude Opus 4.6, GPT 5.4</p>
            </a>
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
                    {article.date && (
                        <time className="article-date">{formatDate(article.date)}</time>
                    )}
                    <p>{article.excerpt}</p>
                </div>
            ))}
        </div>
    );
};

export default ArticlePreview;
