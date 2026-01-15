export const formatDate = (date) => {
  if (!date) return '';

  const d = new Date(date);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  if (d.toDateString() === today.toDateString()) {
    return `Today at ${d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`;
  }

  if (d.toDateString() === yesterday.toDateString()) {
    return `Yesterday at ${d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`;
  }

  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: d.getFullYear() !== today.getFullYear() ? 'numeric' : undefined,
  });
};

export const formatTime = (date) => {
  if (!date) return '';

  const d = new Date(date);
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
};

export const formatRelativeTime = (date) => {
  if (!date) return '';

  const seconds = Math.floor((new Date() - new Date(date)) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;

  return formatDate(date);
};

export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const capitalizeFirstLetter = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const formatMessage = (message) => {
  if (!message) return '';

  // Format markdown bold
  message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Format markdown italic
  message = message.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Format markdown code
  message = message.replace(/`(.*?)`/g, '<code>$1</code>');

  return message;
};

export const extractTextFromMessage = (message) => {
  if (!message) return '';

  let text = message;

  // Remove markdown formatting
  text = text.replace(/\*\*(.*?)\*\*/g, '$1');
  text = text.replace(/\*(.*?)\*/g, '$1');
  text = text.replace(/`(.*?)`/g, '$1');
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  return text;
};
