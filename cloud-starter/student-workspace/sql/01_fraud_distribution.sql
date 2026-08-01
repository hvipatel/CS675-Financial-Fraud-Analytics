SELECT
    is_fraud,
    COUNT(*) AS transaction_count
FROM credit_card_transactions
GROUP BY is_fraud
ORDER BY transaction_count DESC;
