import React from "react";

const QuotaDisplay = ({ quota }) => {
  const getNextResetTime = () => {
    if (!quota?.reset_time) return null;
    const resetDate = new Date(quota.reset_time);
    resetDate.setHours(resetDate.getHours() + 24);
    return resetDate.toLocaleString();
  };

  const isQuotaExhausted = quota?.exercises_remaining === 0;

  return (
    <div className="quota-display">
      <p>Quota: {quota?.exercises_remaining ?? "..."}</p>
      {isQuotaExhausted && <span>Next reset: {getNextResetTime()}</span>}
    </div>
  );
};

export default QuotaDisplay;
