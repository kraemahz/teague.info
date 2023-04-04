import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import ReactMarkdown from "react-markdown";
import "katex/dist/katex.min.css";
import gfm from "remark-gfm";
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import "./Article.css";


interface ArticleProps {
  filePath: string;
}

const Article: React.FC<ArticleProps> = ({ filePath }) => {
  const [content, setContent] = useState("");
  const { id } = useParams<{id: string}>();

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

  return (
    <div className="Article">
      <ReactMarkdown
        children={content}
	remarkPlugins={[gfm, remarkMath]}
	rehypePlugins={[rehypeKatex]}
      />
    </div>
  );
};

export default Article;
