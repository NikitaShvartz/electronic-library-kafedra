<?php

declare(strict_types=1);

namespace Library;

use PDO;
use RuntimeException;

final class Database
{
    public static function connect(): PDO
    {
        $dsn = sprintf(
            'pgsql:host=%s;port=%s;dbname=%s;connect_timeout=3',
            self::environment('DB_HOST'),
            self::environment('DB_PORT'),
            self::environment('DB_NAME'),
        );

        return new PDO($dsn, self::environment('DB_USER'), self::environment('DB_PASSWORD'));
    }

    private static function environment(string $name): string
    {
        $value = getenv($name);
        if ($value === false || $value === '') {
            throw new RuntimeException("Missing environment variable: {$name}");
        }

        return $value;
    }
}
