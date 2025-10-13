use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize)]
struct HealthResponse {
    status: &'static str,
}

#[derive(Debug, Deserialize)]
struct NotificationRequest {
    user_id: String,
    message: String,
}

#[derive(Debug, Serialize)]
struct NotificationResponse {
    id: String,
    user_id: String,
    message: String,
}

#[get("/healthz")]
async fn healthz() -> impl Responder {
    HttpResponse::Ok().json(HealthResponse { status: "ok" })
}

#[post("/notifications")]
async fn send_notification(req: web::Json<NotificationRequest>) -> impl Responder {
    let response = NotificationResponse {
        id: format!("notif-{}", chrono::Utc::now().timestamp_millis()),
        user_id: req.user_id.clone(),
        message: req.message.clone(),
    };
    HttpResponse::Ok().json(response)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port: u16 = std::env::var("PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(8084);
    HttpServer::new(|| App::new().service(healthz).service(send_notification))
        .bind(("0.0.0.0", port))?
        .run()
        .await
}

#[cfg(test)]
mod tests {
    use super::*;
    use actix_web::{body::to_bytes, test, App};

    #[actix_web::test]
    async fn healthz_ok() {
        let app = test::init_service(App::new().service(healthz)).await;
        let req = test::TestRequest::get().uri("/healthz").to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
    }

    #[actix_web::test]
    async fn send_notification_ok() {
        let app = test::init_service(App::new().service(send_notification)).await;
        let payload = NotificationRequest {
            user_id: "user-1".to_string(),
            message: "hello".to_string(),
        };
        let req = test::TestRequest::post()
            .uri("/notifications")
            .set_json(&payload)
            .to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = to_bytes(resp.into_body()).await.unwrap();
        let parsed: NotificationResponse = serde_json::from_slice(&body).unwrap();
        assert_eq!(parsed.user_id, "user-1");
    }
}
