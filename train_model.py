from utils.classifier import (
    load_dataset, split_dataset, vectorize_training_data,
    train_naive_bayes, train_logistic_regression, train_linear_svc,
    evaluate_model, save_model
)
df = load_dataset()
X_train, X_test, y_train, y_test = split_dataset(df)
X_train_vectors, X_test_vectors, vectorizer = vectorize_training_data(X_train, X_test)



print("=== Naive Bayes ===")
nb_model = train_naive_bayes(X_train_vectors, y_train)
accuracy, matrix, report = evaluate_model(nb_model, X_test_vectors, y_test)
print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix:\n{matrix}")
print(f"Report:\n{report}")

print("\n=== Logistic Regression ===")
lr_model = train_logistic_regression(X_train_vectors, y_train)
accuracy, matrix, report = evaluate_model(lr_model, X_test_vectors, y_test)
print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix:\n{matrix}")
print(f"Report:\n{report}")

print("\n=== Linear SVM ===")
svc_model = train_linear_svc(X_train_vectors, y_train)
accuracy, matrix, report = evaluate_model(svc_model, X_test_vectors, y_test)
print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix:\n{matrix}")
print(f"Report:\n{report}")


save_model(svc_model, vectorizer, 'models/resume_classifier.pkl')
print("\nModel saved to models/resume_classifier.pkl")