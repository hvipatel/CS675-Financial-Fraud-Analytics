SELECT
    use_chip AS payment_method,
    COUNT(*) AS fraud_transactions,
    ROUND(
        SUM(
            CAST(
                REPLACE(REPLACE(amount, '$', ''), ',', '')
                AS DOUBLE
            )
        ),
        2
    ) AS fraud_amount
FROM credit_card_transactions
WHERE is_fraud = 'Yes'
GROUP BY use_chip
ORDER BY fraud_transactions DESC;
