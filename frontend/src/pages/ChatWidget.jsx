import React, { useEffect, useRef, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "../assets/ChatWidget.css";
import { postData } from "../services/api"

const API_URL = "http://localhost:8000/api/dashboard/";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, isOpen]);

  async function sendMessage(event) {
    event?.preventDefault();
    const message = input.trim();
    if (!message || loading) return;

    setMessages((current) => [
      ...current,
      { id: Date.now(), text: message, sender: "user" },
    ]);
    setInput("");
    setLoading(true);

    try {

      const data = await postData("chat", {message});

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          text: data.response ?? "The server returned an empty response.",
          sender: "bot",
        },
      ]);
    } catch (error) {
      console.error("Chat API error:", error);
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          text: error.message || "Sorry, something went wrong. Please try again.",
          sender: "bot",
        },
      ]);
    } finally {
      setLoading(false);
    }

  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <>
      {!isOpen && (
        <button
          type="button"
          className="chat-launcher"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
          title="Open chat"
        >
          <i className="bi bi-chat-dots-fill" aria-hidden="true" />
        </button>
      )}

      {isOpen && (
        <section className="chat-widget shadow" aria-label="Chat window">
          <header className="chat-header">
            <div>
              <div className="fw-semibold">
                <i className="bi bi-robot me-2" aria-hidden="true" />
                AI Enquiry Assistant
              </div>
              <small>We are here to help</small>
            </div>
            <button
              type="button"
              className="chat-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              <i className="bi bi-x-lg" aria-hidden="true" />
            </button>
          </header>

          <div className="chat-body" aria-live="polite">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message-row ${
                  message.sender === "user" ? "user-row" : "bot-row"
                }`}
              >
                <div
                  className={`message-bubble ${
                    message.sender === "user" ? "user-message" : "bot-message"
                  }`}
                >
                  {message.text}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row bot-row">
                <div className="message-bubble bot-message typing-indicator">
                  Typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-footer" onSubmit={sendMessage}>
            <textarea
              className="form-control chat-input"
              placeholder="Type your message..."
              aria-label="Type your message"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={loading}
            />
            <button
              type="submit"
              className="btn btn-primary send-button"
              disabled={!input.trim() || loading}
              aria-label="Send message"
            >
              <i className="bi bi-send-fill" aria-hidden="true" />
            </button>
          </form>
        </section>
      )}
    </>
  );
}
