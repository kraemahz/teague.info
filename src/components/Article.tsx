import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import ReactMarkdown from "react-markdown";
import "katex/dist/katex.min.css";
import gfm from "remark-gfm";
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

import "./Article.css";
import MetaTags from "./MetaTags";

interface ArticleProps {
  filePath: string;
}

const Article: React.FC<ArticleProps> = ({ filePath }) => {
  const [content, setContent] = useState("");
  const [article, setArticle] = useState({
    id: "", title: "", excerpt: "", image: ""
  });
  const { id } = useParams<{id: string}>();

  useEffect(() => {
    fetch("/articles/articleList.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch the article list");
        }
        return response.json();
      })
      .then((data) => {
        for(let obj of data) {
          if (obj.id === id) {
            return obj;
          }
        }
        return null;
      })
      .then((data) => setArticle(data))
      .catch((error) => console.error(error));
  }, []);

  useEffect(() => {
    fetch(`${filePath}/${id}.md`)
      .then((response) => {
        if (!response.ok) {
	  throw new Error("Failed to fetch the article");
	}

	return response.text();
      })
      .then((text) => setContent(text))
      .catch((error) => console.error(error));
  }, [id, filePath]);
  const image = `/images/${article.image}`;

  return (
    <div className="Article">
      <MetaTags article={article} />
      <img src={image} />
      <ReactMarkdown
        children={content}
        remarkPlugins={[gfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
      />
    </div>
  );
};

export default Article;
