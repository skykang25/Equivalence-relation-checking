"""집합 A = {1, 2, 3, 4, 5} 위의 동치관계와 폐포를 조사한다."""

SIZE = 5


def read_matrix():
    """각 행을 검증한 뒤 정수로 바꾸어 2차원 리스트에 저장한다."""
    matrix = []
    while len(matrix) < SIZE:
        row = input(f"{len(matrix) + 1}행> ").split()
        if len(row) != SIZE or any(x not in ("0", "1") for x in row):
            print("입력 오류: 0 또는 1을 공백으로 구분해 5개 입력하세요.")
            continue  # 잘못된 행은 저장하지 않고 같은 행을 다시 받는다.
        matrix.append([int(x) for x in row])
    return matrix


def is_reflexive(m):
    return all(m[i][i] == 1 for i in range(len(m)))


def is_symmetric(m):
    # 대각선을 기준으로 마주 보는 칸은 한 번씩만 비교한다.
    n = len(m)
    return all(m[i][j] == m[j][i] for i in range(n) for j in range(i))


def is_transitive(m):
    # i → k, k → j가 있는데 i → j가 없으면 추이성의 반례다.
    n = len(m)
    for i in range(n):
        for k in range(n):
            for j in range(n):
                if m[i][k] and m[k][j] and not m[i][j]:
                    return False
    return True


def equivalence_class(m, a):
    """동치관계에서 원소 a와 관계있는 모든 원소를 구한다."""
    return [j for j, value in enumerate(m[a - 1], start=1) if value]


def reflexive_closure(m):
    result = [row[:] for row in m]
    for i in range(len(m)):
        result[i][i] = 1
    return result


def symmetric_closure(m):
    result = [row[:] for row in m]
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j]:
                result[j][i] = 1
    return result


def transitive_closure(m):
    # 워셜 알고리즘: 중간 원소 k를 하나씩 허용하며 경로를 늘린다.
    result = [row[:] for row in m]
    n = len(m)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if result[i][k] and result[k][j]:
                    result[i][j] = 1
    return result


def added_pairs(before, after):
    # 행렬 인덱스가 아닌 집합 A의 원소 번호로 변화량을 기록한다.
    return [(i + 1, j + 1) for i in range(len(before))
            for j in range(len(before)) if not before[i][j] and after[i][j]]


def show_status(m):
    checks = (is_reflexive(m), is_symmetric(m), is_transitive(m))
    verdict = "동치관계" if all(checks) else "동치관계 아님"
    marks = ["O" if ok else "X" for ok in checks]
    print(f"반사 {marks[0]} / 대칭 {marks[1]} / 추이 {marks[2]} : {verdict}")
    if all(checks):
        for a in range(1, len(m) + 1):
            members = ", ".join(map(str, equivalence_class(m, a)))
            print(f"[{a}] = {{{members}}}")
    return checks


def show_change(title, before, after):
    print(f"\n[{title}]")
    print("변환 전 R        변환 후")
    for left, right in zip(before, after):
        print(" ".join(map(str, left)), "      ", " ".join(map(str, right)), sep="")
    added = added_pairs(before, after)
    print(f"추가한 순서쌍 {len(added)}개:")
    for start in range(0, len(added), 6):
        print(" ".join(f"({i},{j})" for i, j in added[start:start + 6]))
    show_status(after)


def main():
    print("동치관계 판별 | A = {1, 2, 3, 4, 5}")
    print("각 행에 0 또는 1을 공백으로 구분해 5개 입력하세요.")
    m = read_matrix()
    print("\n[원래 관계]")
    checks = show_status(m)
    closures = (("반사폐포", reflexive_closure), ("대칭폐포", symmetric_closure),
                ("추이폐포", transitive_closure))
    for ok, (title, close) in zip(checks, closures):
        if not ok:
            # 각 폐포의 출발점은 동일한 원본이다.
            show_change(title, m, close(m))
    if checks.count(False) >= 2:
        # 독립 폐포와 별도로 세 성질을 모두 갖는 최소 확장을 보여 준다.
        eq = transitive_closure(symmetric_closure(reflexive_closure(m)))
        show_change("추가 기능: 동치폐포", m, eq)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        raise SystemExit("입력 종료: 5개 행이 모두 입력되지 않았습니다.")
