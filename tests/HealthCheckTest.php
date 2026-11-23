<?php

declare(strict_types=1);

namespace Library\Tests;

use Library\HealthCheck;
use PDO;
use PDOException;
use PDOStatement;
use PHPUnit\Framework\TestCase;

final class HealthCheckTest extends TestCase
{
    public function testReturnsOkWhenDatabaseResponds(): void
    {
        $database = $this->createMock(PDO::class);
        $database->expects($this->once())->method('query')->with('SELECT 1')
            ->willReturn($this->createStub(PDOStatement::class));

        self::assertSame(200, HealthCheck::statusCode(static fn (): PDO => $database));
    }

    public function testReturnsUnavailableWhenConnectionFails(): void
    {
        self::assertSame(503, HealthCheck::statusCode(static function (): PDO {
            throw new PDOException('Connection refused');
        }));
    }
}
