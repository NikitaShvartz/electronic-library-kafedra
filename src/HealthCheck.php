<?php

declare(strict_types=1);

namespace Library;

final class HealthCheck
{
    public static function statusCode(callable $connect): int
    {
        try {
            $connect()->query('SELECT 1');

            return 200;
        } catch (\RuntimeException) {
            error_log('Library health check failed: database unavailable');

            return 503;
        }
    }
}
