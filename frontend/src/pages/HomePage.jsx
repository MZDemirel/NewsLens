import { useEffect, useState } from "react";
import NewsList from "../components/NewsList";
import api from "../api/client";

export default function HomePage() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get("/news/")
      .then((res) => setNews(res.data))
      .catch(() => setError("Haberler yüklenemedi."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Yükleniyor...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h2>Son Haberler</h2>
      <NewsList items={news} />
    </div>
  );
}
