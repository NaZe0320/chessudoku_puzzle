#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import delete_puzzle

def delete_puzzle_by_id(puzzle_id):
    """특정 퍼즐 ID 삭제"""
    print(f"\n퍼즐 ID {puzzle_id} 삭제 요청 중...")
    success, result = delete_puzzle(puzzle_id)
    
    if success:
        print(f"✅ 퍼즐 {puzzle_id} 삭제 성공!")
    else:
        print(f"❌ 퍼즐 {puzzle_id} 삭제 실패!")
    
    return success, result

def delete_multiple_puzzles(puzzle_ids):
    """여러 퍼즐 ID 삭제"""
    print("=" * 60)
    print(f"퍼즐 삭제 요청 시작 (ID: {', '.join(puzzle_ids)})")
    print("=" * 60)
    
    results = []
    
    for puzzle_id in puzzle_ids:
        success, result = delete_puzzle_by_id(puzzle_id)
        results.append((puzzle_id, success, result))
    
    print("\n" + "=" * 60)
    print("삭제 요청 결과 요약")
    print("=" * 60)
    
    for puzzle_id, success, result in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"퍼즐 ID {puzzle_id}: {status}")
        if result:
            print(f"  응답: {result}")
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 명령행 인수로 퍼즐 ID들 받기
        puzzle_ids = sys.argv[1:]
        delete_multiple_puzzles(puzzle_ids)
    else:
        # 기본적으로 퍼즐 ID 9 삭제
        delete_puzzle_by_id('9')
