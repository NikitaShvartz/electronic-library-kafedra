<?php

declare(strict_types=1);

use Library\Database;
use Library\HealthCheck;

require_once __DIR__ . '/../src/Database.php';
require_once __DIR__ . '/../src/HealthCheck.php';

header('Content-Type: application/json; charset=utf-8');

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);

switch ($path) {
    case '/':
        $response = ['name' => 'Электронная библиотека кафедры'];
        break;
    case '/health':
        $status = HealthCheck::statusCode(Database::connect(...));
        http_response_code($status);
        $response = ['status' => $status === 200 ? 'ok' : 'unavailable'];
        break;
    default:
        http_response_code(404);
        $response = ['error' => 'not_found'];
}

echo json_encode($response, JSON_UNESCAPED_UNICODE);
