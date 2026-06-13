import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/client";

export default function NewsDetailPage() {
  const { id } = useParams();
  const [news, setNews] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get(`/news/${id}`)
      .then((res) => setNews(res.data))
      .catch(() => setError("Haber bulunamadı."))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>Yükleniyor...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <Link to="/">&larr; Geri</Link>
      <h2>{news.title}</h2>
      <div style={{ color: "#888", fontSize: 13, marginBottom: 12 }}>
        {news.source} {news.category && `• ${news.category}`}
      </div>
      {news.summary && <p><strong>{news.summary}</strong></p>}
      {news.full_text && <p>{news.full_text}</p>}
      <a href={news.url} target="_blank" rel="noreferrer">Kaynağa git</a>
    </div>
  );
}
