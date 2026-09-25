import { useState } from "react";
import API, { uploadPDF } from "./api";

function App() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);

  const [uploadStatus, setUploadStatus] = useState("");

  async function askAI() {
    if (!question.trim()) return;

    const currentQuestion = question;

    setMessages((prev) => [
      ...prev,

      {
        role: "user",
        text: currentQuestion,
      },
    ]);

    setQuestion("");

    setLoading(true);

    try {
      const res = await API.post(
        "/ask",

        {
          question: currentQuestion,
        },
      );

      setMessages((prev) => [
        ...prev,

        {
          role: "assistant",

          text: res.data.answer || "No answer generated.",

          sources: res.data.sources || [],

          security: res.data.security,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,

        {
          role: "assistant",

          text: "⚠️ Unable to connect with ShadowMemory server.",
        },
      ]);
    }

    setLoading(false);
  }

  async function handleUpload(e) {
    const file = e.target.files[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setUploadStatus("❌ Only PDF files allowed");

      return;
    }

    setUploading(true);

    setUploadStatus("Uploading and indexing document...");

    try {
      const res = await uploadPDF(file);

      setUploadStatus(
        "✅ " + (res.data.message || `${res.data.file} uploaded successfully`),
      );
    } catch (error) {
      setUploadStatus("❌ Upload failed");
    }

    setUploading(false);
  }

  return (
    <div
      className="
flex
h-screen
bg-[#0B1220]
text-white
"
    >
      {/* SIDEBAR */}

      <div
        className="
hidden
md:flex
flex-col
w-72
bg-[#111827]
border-r
border-blue-500/20
p-6
"
      >
        <h1
          className="
text-3xl
font-bold
bg-gradient-to-r
from-blue-400
to-cyan-400
bg-clip-text
text-transparent
"
        >
          ShadowMemory
        </h1>

        <p
          className="
text-gray-400
mt-2
"
        >
          Enterprise AI Assistant
        </p>

        <div
          className="
mt-10
space-y-4
"
        >
          <div
            className="
bg-blue-500/15
border
border-blue-400/30
rounded-xl
p-4
"
          >
            🤖
            <p className="text-sm mt-2">RAG + Gemini</p>
          </div>

          <div
            className="
bg-blue-500/15
border
border-blue-400/30
rounded-xl
p-4
"
          >
            🛡️
            <p className="text-sm mt-2">ShadowMemory Security</p>
          </div>

          <div
            className="
bg-blue-500/15
border
border-blue-400/30
rounded-xl
p-4
"
          >
            📚
            <p className="text-sm mt-2">Company Knowledge Base</p>
          </div>

          {/* UPLOAD */}

          <div
            className="
bg-[#1E293B]
border
border-blue-400/30
rounded-xl
p-4
"
          >
            <p
              className="
text-sm
font-semibold
mb-3
"
            >
              📄 Upload PDF
            </p>

            <label
              className="
block
cursor-pointer
bg-gradient-to-r
from-blue-500
to-cyan-500
rounded-lg
py-2
text-center
text-sm
font-semibold
"
            >
              {uploading ? "Uploading..." : "Choose PDF"}

              <input
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={handleUpload}
              />
            </label>

            {uploadStatus && (
              <p
                className="
text-xs
text-gray-300
mt-3
"
              >
                {uploadStatus}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* MAIN */}

      <div
        className="
flex-1
flex
flex-col
"
      >
        <div
          className="
p-5
bg-[#111827]
border-b
border-blue-500/20
"
        >
          <h2
            className="
text-2xl
font-semibold
"
          >
            ShadowMemory AI
          </h2>

          <p
            className="
text-gray-400
text-sm
"
          >
            Secure document intelligence platform
          </p>
        </div>

        {/* CHAT */}

        <div
          className="
flex-1
overflow-y-auto
p-6
space-y-6
"
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className={
                msg.role === "user" ? "flex justify-end" : "flex justify-start"
              }
            >
              <div
                className={
                  msg.role === "user"
                    ? `
max-w-xl
bg-gradient-to-r
from-blue-500
to-cyan-500
p-3
rounded-2xl
text-sm
`
                    : `
max-w-3xl
bg-[#1E293B]
border
border-blue-400/20
rounded-2xl
p-4
text-sm
`
                }
              >
                <p
                  className="
whitespace-pre-line
leading-relaxed
"
                >
                  {msg.text}
                </p>

                {/* SECURITY PANEL */}

                {msg.security && (
                  <div
                    className="
mt-4
pt-4
border-t
border-blue-400/20
space-y-3
"
                  >
                    <div
                      className="
flex
gap-2
flex-wrap
"
                    >
                      <span
                        className="
bg-green-500/20
text-green-400
px-3
py-1
rounded-full
text-xs
"
                      >
                        🛡 {msg.security.risk_level}
                      </span>

                      <span
                        className="
bg-blue-500/20
text-blue-300
px-3
py-1
rounded-full
text-xs
"
                      >
                        Risk {msg.security.risk_score}
                      </span>

                      <span
                        className="
bg-cyan-500/20
text-cyan-300
px-3
py-1
rounded-full
text-xs
"
                      >
                        Trust {msg.security.trust_score}
                      </span>
                    </div>

                    {/* REMOVED CONTENT */}

                    {msg.security.removed_content?.length > 0 && (
                      <div
                        className="
bg-red-500/10
border
border-red-400/30
rounded-xl
p-3
"
                      >
                        <p
                          className="
text-red-400
font-semibold
text-xs
mb-2
"
                        >
                          🚨 Removed Malicious Instructions
                        </p>

                        <ul
                          className="
text-xs
text-gray-300
list-disc
ml-5
"
                        >
                          {msg.security.removed_content.map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* SANITIZED CONTEXT */}

                    {msg.security.sanitized_context && (
                      <div
                        className="
bg-green-500/10
border
border-green-400/30
rounded-xl
p-3
"
                      >
                        <p
                          className="
text-green-400
font-semibold
text-xs
mb-2
"
                        >
                          ✅ Sanitized Document Context
                        </p>

                        <p
                          className="
text-xs
text-gray-300
max-h-32
overflow-y-auto
whitespace-pre-line
"
                        >
                          {msg.security.sanitized_context}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div
              className="
bg-blue-500/20
rounded-xl
px-4
py-3
w-fit
animate-pulse
text-sm
"
            >
              ShadowMemory is thinking...
            </div>
          )}
        </div>

        {/* INPUT */}

        <div
          className="
p-5
bg-[#111827]
border-t
border-blue-500/20
"
        >
          <div
            className="
flex
gap-3
bg-[#1E293B]
border
border-blue-400/30
rounded-2xl
p-3
"
          >
            <input
              className="
flex-1
bg-transparent
outline-none
px-4
"
              placeholder="
Ask anything about company documents...
"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") askAI();
              }}
            />

            <button
              onClick={askAI}
              className="
bg-gradient-to-r
from-blue-500
to-cyan-500
px-7
rounded-xl
font-semibold
"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
